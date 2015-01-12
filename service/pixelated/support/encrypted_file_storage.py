#
# Copyright (c) 2014 ThoughtWorks, Inc.
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.

import io
from hashlib import sha512

import os
from whoosh.filedb.filestore import FileStorage
from whoosh.filedb.structfile import StructFile, BufferFile
from nacl.secret import SecretBox
import nacl.utils
from whoosh.util import random_name


class EncryptedFileStorage(FileStorage):
    def __init__(self, path, masterkey=None):
        self.masterkey = masterkey
        self.secret_box = SecretBox(masterkey)
        self._tmp_storage = self.temp_storage
        self.length_cache = {}
        FileStorage.__init__(self, path, supports_mmap=False)

    def open_file(self, name, **kwargs):
        return self._open_encrypted_file(name, onclose=self._encrypt_index_on_close(name))

    def create_file(self, name, excl=False, mode="w+b", **kwargs):
        f = StructFile(io.BytesIO(), name=name, onclose=self._encrypt_index_on_close(name))
        f.is_real = False
        return f

    def temp_storage(self, name=None):
        name = name or "%s.tmp" % random_name()
        path = os.path.join(self.folder, name)
        return EncryptedFileStorage(path, self.masterkey).create()

    def file_length(self, name):
        return self.length_cache[name][0]

    @property
    def _nonce(self):
        return nacl.utils.random(SecretBox.NONCE_SIZE)

    def _encrypt_index_on_close(self, name):
        def wrapper(struct_file):
            struct_file.seek(0)
            content = struct_file.file.read()
            file_hash = sha512(content).digest()
            if name in self.length_cache and file_hash == self.length_cache[name][1]:
                return
            self.length_cache[name] = (len(content), file_hash)
            encrypted_content = self.secret_box.encrypt(content, self._nonce)
            with open(self._fpath(name), 'w+b') as f:
                f.write(encrypted_content)
        return wrapper

    def _open_encrypted_file(self, name, onclose=lambda x: None):
        file_content = open(self._fpath(name), "rb").read()
        decrypted = self.secret_box.decrypt(file_content)
        self.length_cache[name] = (len(decrypted), sha512(decrypted).digest())
        return BufferFile(buffer(decrypted), name=name, onclose=onclose)
