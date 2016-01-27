from twisted.web.server import Site, Request


class AddCSPHeaderRequest(Request):
    HEADER_VALUES = "default-src 'self'; style-src 'self' 'unsafe-inline'"

    def process(self):
        self.setHeader("Content-Security-Policy", self.HEADER_VALUES)
        self.setHeader("X-Content-Security-Policy", self.HEADER_VALUES)
        self.setHeader("X-Webkit-CSP", self.HEADER_VALUES)
        Request.process(self)


class PixelatedSite(Site):

    requestFactory = AddCSPHeaderRequest

    @classmethod
    def enable_csp_requests(cls):
        cls.requestFactory = Site.requestFactory

    @classmethod
    def disable_csp_requests(cls):
        cls.requestFactory = AddCSPHeaderRequest
