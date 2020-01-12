import stem
from stem.descriptor import DocumentHandler
from stem.descriptor.remote import DescriptorDownloader

downloader = DescriptorDownloader()
v3 = '3E1A10AE784EEC2222402D54EF3304F6E1DB6384'
endpoints = [stem.DirPort('127.0.0.1',7000)]
consensus = downloader.get_consensus(authority_v3ident=v3, endpoints=endpoints, document_handler=DocumentHandler.DOCUMENT).run()[0]

for fingerprint, relay in consensus.routers.items():
  print("%s: %s" % (fingerprint, relay.nickname))
