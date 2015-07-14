import leap.soledad.client as client
import urlparse
from leap.soledad.client.events import (
    SOLEDAD_DONE_DATA_SYNC,
    signal
)


def patched_sync(self, defer_decryption=True):
    if self._db:
        try:
            local_gen = self._db.sync(
                urlparse.urljoin(self.server_url, 'user-%s' % self._uuid),
                creds=self._creds, autocreate=False,
                defer_decryption=defer_decryption)
            signal(SOLEDAD_DONE_DATA_SYNC, self._uuid)
            return local_gen
        except Exception as e:
            client.logger.error("Soledad exception when syncing: %s - %s" % (e.__class__.__name__, e.message))


# client.Soledad.sync = patched_sync
