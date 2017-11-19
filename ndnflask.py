import json
import pyndn as ndn
import pyndn.security as ndnsec
import sys
try:
    import asyncio
except ImportError:
    import trollius as asyncio
from pyndn.threadsafe_face import ThreadsafeFace
import logging
logging.basicConfig()
import sys
import time
import argparse
import traceback
import random

from pyndn import Name
from pyndn import Data
from pyndn import Face
from pyndn.security import KeyChain


class Flask():
  def __init__(self, host):
      self.__name__ = __name__
      self.keyChain = KeyChain()
      self.isDone = False
      self.counter = 0
      loop = asyncio.get_event_loop()
      self.face = ThreadsafeFace(loop, host)
      self.a = {}
      self.methods = {}

  def route(self, uri, methods):
      self.baseName = ndn.Name(uri) 
      self.methods[self.baseName]=methods[0]
      return self.dec 

  def onInterest(self, prefix, interest, *k):
      print >> sys.stderr, "<< PyNDN %s" % interest.name
      print prefix
      d = self.a[prefix]
      if self.methods[prefix] == "POST":
         content = json.dumps(d(interest.getContent().toRawStr().decode('string_escape')))
      else:
         content = json.dumps(d())
      self.counter += 1
      #print interest.getContent().toRawStr().decode('string_escape')
      data = ndn.Data(interest.getName())

      meta = ndn.MetaInfo()
      meta.setFreshnessPeriod(5000)
      data.setMetaInfo(meta)

      data.setContent(content)
      self.keyChain.sign(data, self.keyChain.getDefaultCertificateName())

      self.face.putData(data)

  def _onRegisterFailed(self, prefix):
      print >> sys.stderr, "<< PyNDN: failed to register prefix"

  def run(self):
      root = logging.getLogger()
      root.setLevel(logging.DEBUG)

      ch = logging.StreamHandler(sys.stdout)
      ch.setLevel(logging.DEBUG)
      formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
      ch.setFormatter(formatter)
      root.addHandler(ch)
      loop = asyncio.get_event_loop()
      #face = ThreadsafeFace(loop, "172.17.0.1")
      #face = ndn.Face("172.17.0.1","6363")
      server = Server(self.face)

      loop.run_forever()
      face.shutdown()
      

  def dec(self,func): 
      self.a[self.baseName] = func
      print self.a
      self.face.registerPrefix(self.baseName,
                               self.onInterest, self._onRegisterFailed,)

class Server:
  def __init__(self, face):
      self.face = face
      self.counter = 0
      self.keyChain = ndnsec.KeyChain()
      #self.keyChain._setDefaultCertificate()
      #self.identity = ndn.Name("/ndn/edu/ucla/alice");
      #certificateName = keyChain.createIdentity(identity);
      #self.alice = self.keyChain.createIdentity(self.identity)
      #aliceKeyName = self.keyChain.generateRSAKeyPair(alice)
      #self.keyChain.setDefaultKeyNameForIdentity(alice)
      #self.keyChain.setDefaultIdentity(self.alice)
      self.face.setCommandSigningInfo(self.keyChain, self.keyChain.getDefaultCertificateName())
      #self.face.registerPrefix(self.baseName1,
      #                         self._onInterest, self._onRegisterFailed)
      #self.face.registerPrefix(self.baseName2,
      #                         self._onInterest, self._onRegisterFailed)


