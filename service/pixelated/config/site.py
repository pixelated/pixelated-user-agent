from twisted.web.server import Site, Request


class AddCSPHeaderRequest(Request):
    def process(self):
        self.setHeader("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline'")
        Request.process(self)


class PixelatedSite(Site):
    requestFactory = AddCSPHeaderRequest
