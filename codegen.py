import os
from grpc_tools import protoc

script_path = os.path.dirname(os.path.abspath(__file__))

# Localizer service
protoc.main((
    '',
    '-I%s'%(script_path),
    '--python_out=%s/'%(script_path),
    '--grpc_python_out=%s/'%(script_path),
    '%s/localizer.proto'%(script_path),
))

