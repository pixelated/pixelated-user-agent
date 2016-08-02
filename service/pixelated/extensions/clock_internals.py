from pixelated.support.clock import Clock

from leap.mail.incoming.service import IncomingMail
def _sync_soledad_with_clock(funct):
    def wrapper(*args, **kwargs):
        t1 = Clock('sync-leap-mail-recurrent', args[0]._soledad.uuid)
        def after(param):
            t1.stop()
            return param
        d = funct(*args, **kwargs)
        d.addCallbacks(after,after)
        return d
    return wrapper
IncomingMail._sync_soledad = _sync_soledad_with_clock(IncomingMail._sync_soledad)

from leap.soledad.client.http_target.send import HTTPDocSender
def _send_docs_with_clock(funct):
    def wrapper(*args, **kwargs):
        t1 = Clock('sync-soledad-upload-docs', args[0].uuid)
        def after(param):
            t1.stop()
            return param
        d = funct(*args, **kwargs)
        d.addCallbacks(after,after)
        return d
    return wrapper
HTTPDocSender._send_docs = _send_docs_with_clock(HTTPDocSender._send_docs)


from leap.soledad.client.http_target.fetch import HTTPDocFetcher
def _receive_docs_with_clock(funct):
    def wrapper(*args, **kwargs):
        t1 = Clock('sync-soledad-download-docs', args[0].uuid)
        def after(param):
            t1.stop()
            return param
        d = funct(*args, **kwargs)
        d.addCallbacks(after,after)
        return d
    return wrapper
HTTPDocFetcher._receive_docs = _receive_docs_with_clock(HTTPDocFetcher._receive_docs)


from leap.soledad.client.http_target.api import SyncTargetAPI
def _get_sync_info_with_clock(funct):
    def wrapper(*args, **kwargs):
        t1 = Clock('sync-soledad-get-remote-state', args[0]._uuid)
        def after(param):
            t1.stop()
            return param
        d = funct(*args, **kwargs)
        d.addCallbacks(after,after)
        return d
    return wrapper
SyncTargetAPI.get_sync_info = _get_sync_info_with_clock(SyncTargetAPI.get_sync_info)


from leap.soledad.common.l2db.backends.sqlite_backend import SQLiteDatabase
def _whats_changed_with_clock(funct):
    def wrapper(*args, **kwargs):
        t1 = Clock('sync-soledad-diff-docs')
        data = funct(*args, **kwargs)
        t1.stop()
        return data
    return wrapper
SQLiteDatabase.whats_changed = _whats_changed_with_clock(SQLiteDatabase.whats_changed)
