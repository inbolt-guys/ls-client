import localizer_pb2 
import localizer_pb2_grpc 
import grpc
from scipy.spatial.transform import Rotation as R
import numpy as np

def convert_frame(frame) :
    """
    Convert a tracking frame in a Transformation matric 
    
    Parameters
    ----------
    frame : localizer_pb2.PoseMessage
        Tracking frame comming frome the tracking micro service.

    Returns
    -------
    T : np.array
        Tranformation matrix between the coordinate frame of the camera and the cad model.

    """
    trans = frame.translation #position of the camera in x,y,z in the coordinate system of the cad model
    rot = frame.rotation #rotation of the camera in the coordinate system of the cad model
    T = np.eye(4)
    T[:3,:3] = R.from_quat([rot.x, rot.y, rot.z, rot.w]).as_matrix()
    T[:3,3] = np.array([trans.x, trans.y, trans.z])
    return T



ls_addr = '0.0.0.0:5053' #ip address of the micro service most likely localhost
ls_channel = grpc.insecure_channel(ls_addr)
ls_stub = localizer_pb2_grpc.LocalizerStub(ls_channel)
frames = ls_stub.GetPose(localizer_pb2.EmptyMessage())
for frame in frames:
    T = convert_frame(frame)
    t = frame.timestamp
    print("translation %s"%list(T[:3,3]))