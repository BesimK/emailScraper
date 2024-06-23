import re
import aiohttp
import asyncio
from urllib.parse import urlsplit, urljoin, urldefrag
from lxml import html


class EmailCrawler:
    def __init__(self, website: str, max_pages=50, semaphore=10):
        self.website = website
        self.base_url = urlsplit(self.website).netloc
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                          'Chromium/78.0.3904.70 Chrome/78.0.3904.70 Safari/537.36',
        }
        self.garbage_extensions = ['.aif', '.cda', '.mid', '.midi', '.mp3', '.mp4', '.mpa', '.mov', '.webm', '.ogg',
                                   '.wav', '.wma', '.wpl', '.7z', '.arj', '.deb', '.pkg', '.rar', '.rpm', '.tar.gz',
                                   '.z', '.zip', '.bin', '.dmg', '.iso', '.toast', '.vcd', '.csv', '.dat', '.db',
                                   '.dbf', '.log', '.mdb', '.sav', '.sql', '.tar', '.apk', '.bat', '.bin', '.cgi',
                                   '.pl', '.exe', '.gadget', '.jar', '.py', '.wsf', '.fnt', '.fon', '.otf', '.ttf',
                                   '.ai', '.bmp', '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg',
                                   '.tif', '.tiff', '.asp', '.cer', '.cfm', '.cgi', '.pl', '.part', '.py', '.rss',
                                   '.key', '.odp', '.pps', '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h',
                                   '.java', '.sh', '.swift', '.vb', '.ods', '.xlr', '.xls', '.xlsx', '.bak', '.cab',
                                   '.cfg', '.cpl', '.cur', '.dll', '.dmp', '.drv', '.icns', '.ico', '.ini', '.lnk',
                                   '.msi', '.sys', '.tmp', '.3g2', '.3gp', '.avi', '.flv', '.h264', '.m4v', '.mkv',
                                   '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                                   '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wks', '.wps', '.wpd']
        self.emails = set()
        self.email_count = 0
        self.max_pages = max_pages
        self.semaphore = asyncio.Semaphore(semaphore)  # Limit concurrent HTTP requests
        self.processed_urls = set()
        self.url_queue = asyncio.Queue()
        self.queued_urls = set()

    def get_emails(self):
        return asyncio.run(self._crawl())

    async def _crawl(self):
        async with aiohttp.ClientSession() as session:
            normalized_start_url = self._normalize_url(self.website)
            await self.url_queue.put(normalized_start_url)
            self.queued_urls.add(normalized_start_url)
            workers = [asyncio.create_task(self.worker(session)) for _ in range(10)]
            await self.url_queue.join()
            for worker in workers:
                worker.cancel()
        print('End of crawling for {} '.format(self.website))
        print('Total urls visited {}'.format(len(self.processed_urls)))
        print('Total Emails found {}'.format(self.email_count))
        return self.emails

    async def worker(self, session):
        while True:
            current_url = await self.url_queue.get()
            try:
                await self._crawl_website(session, current_url)
            finally:
                self.url_queue.task_done()

    async def _crawl_website(self, session, current_url):
        async with self.semaphore:
            normalized_url = self._normalize_url(current_url)
            if normalized_url in self.processed_urls or \
                    (self.max_pages is not None and len(self.processed_urls) >= self.max_pages):
                return

            print("Crawling -> {}".format(current_url))
            self.processed_urls.add(normalized_url)

            try:
                async with session.get(normalized_url, headers=self.headers) as response:
                    if response.status == 200 and 'text/html' in response.headers.get('Content-Type', ''):
                        text = await response.text()
                        self._parse_emails(text)
                        await self._parse_sub_urls(normalized_url, text)
            except Exception as e:
                print(f"Error crawling {current_url}: {e}")

    async def _parse_sub_urls(self, current_url, text):
        tree = html.fromstring(text)
        urls = tree.xpath('//a/@href')
        urls = [urljoin(current_url, url) for url in urls]
        urls = [self._normalize_url(url) for url in urls]
        urls = [url for url in urls if urlsplit(url).netloc == self.base_url]
        unique_urls = set(urls)

        for url in unique_urls:
            if url not in self.processed_urls and url not in self.queued_urls:
                await self.url_queue.put(url)
                self.queued_urls.add(url)

    def _parse_emails(self, text):
        emails = set(re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z-.]+', text, re.I))
        for email in emails:
            if not any(email.endswith(ext) for ext in self.garbage_extensions):
                if email not in self.emails:
                    self.email_count += 1
                    self.emails.add(email)
                    print(' {}. Email found {}'.format(self.email_count, email))

    def _normalize_url(self, url):
        url = urldefrag(url)[0]  # Remove fragment
        url_parts = urlsplit(url)
        normalized_url = url_parts._replace(path=url_parts.path.rstrip('/')).geturl()
        return normalized_url
