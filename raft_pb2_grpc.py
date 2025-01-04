# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import raft_pb2 as raft__pb2

GRPC_GENERATED_VERSION = '1.66.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in raft_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class RaftServiceStub(object):
    """Service definition
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.login = channel.unary_unary(
                '/RaftService/login',
                request_serializer=raft__pb2.LoginRequest.SerializeToString,
                response_deserializer=raft__pb2.LoginResponse.FromString,
                _registered_method=True)
        self.logout = channel.unary_unary(
                '/RaftService/logout',
                request_serializer=raft__pb2.LogoutRequest.SerializeToString,
                response_deserializer=raft__pb2.LogoutResponse.FromString,
                _registered_method=True)
        self.uploadFile = channel.unary_unary(
                '/RaftService/uploadFile',
                request_serializer=raft__pb2.UploadRequest.SerializeToString,
                response_deserializer=raft__pb2.UploadResponse.FromString,
                _registered_method=True)
        self.downloadFile = channel.unary_unary(
                '/RaftService/downloadFile',
                request_serializer=raft__pb2.DownloadRequest.SerializeToString,
                response_deserializer=raft__pb2.DownloadResponse.FromString,
                _registered_method=True)
        self.getAssignments = channel.unary_unary(
                '/RaftService/getAssignments',
                request_serializer=raft__pb2.GetRequest.SerializeToString,
                response_deserializer=raft__pb2.GetResponse.FromString,
                _registered_method=True)
        self.askQuery = channel.unary_unary(
                '/RaftService/askQuery',
                request_serializer=raft__pb2.QueryRequest.SerializeToString,
                response_deserializer=raft__pb2.QueryResponse.FromString,
                _registered_method=True)
        self.getQueries = channel.unary_unary(
                '/RaftService/getQueries',
                request_serializer=raft__pb2.QueryListRequest.SerializeToString,
                response_deserializer=raft__pb2.QueryListResponse.FromString,
                _registered_method=True)
        self.replyQuery = channel.unary_unary(
                '/RaftService/replyQuery',
                request_serializer=raft__pb2.ReplyQueryRequest.SerializeToString,
                response_deserializer=raft__pb2.ReplyQueryResponse.FromString,
                _registered_method=True)
        self.gptQuery = channel.unary_unary(
                '/RaftService/gptQuery',
                request_serializer=raft__pb2.GPTQueryRequest.SerializeToString,
                response_deserializer=raft__pb2.GPTQueryResponse.FromString,
                _registered_method=True)
        self.RequestVote = channel.unary_unary(
                '/RaftService/RequestVote',
                request_serializer=raft__pb2.RequestVoteRequest.SerializeToString,
                response_deserializer=raft__pb2.RequestVoteResponse.FromString,
                _registered_method=True)
        self.AppendEntries = channel.unary_unary(
                '/RaftService/AppendEntries',
                request_serializer=raft__pb2.AppendEntriesRequest.SerializeToString,
                response_deserializer=raft__pb2.AppendEntriesResponse.FromString,
                _registered_method=True)
        self.GetLeader = channel.unary_unary(
                '/RaftService/GetLeader',
                request_serializer=raft__pb2.Empty.SerializeToString,
                response_deserializer=raft__pb2.GetLeaderResponse.FromString,
                _registered_method=True)
        self.Suspend = channel.unary_unary(
                '/RaftService/Suspend',
                request_serializer=raft__pb2.SuspendRequest.SerializeToString,
                response_deserializer=raft__pb2.Empty.FromString,
                _registered_method=True)
        self.SetVal = channel.unary_unary(
                '/RaftService/SetVal',
                request_serializer=raft__pb2.SetValRequest.SerializeToString,
                response_deserializer=raft__pb2.SetValResponse.FromString,
                _registered_method=True)
        self.GetVal = channel.unary_unary(
                '/RaftService/GetVal',
                request_serializer=raft__pb2.GetValRequest.SerializeToString,
                response_deserializer=raft__pb2.GetValResponse.FromString,
                _registered_method=True)
        self.SendSome = channel.unary_unary(
                '/RaftService/SendSome',
                request_serializer=raft__pb2.sendsomethingproto.SerializeToString,
                response_deserializer=raft__pb2.sendresponse.FromString,
                _registered_method=True)
        self.getsome = channel.unary_unary(
                '/RaftService/getsome',
                request_serializer=raft__pb2.getrajivRequest.SerializeToString,
                response_deserializer=raft__pb2.getrajivResponse.FromString,
                _registered_method=True)
        self.nonsenseservice = channel.unary_unary(
                '/RaftService/nonsenseservice',
                request_serializer=raft__pb2.nonsenserequest.SerializeToString,
                response_deserializer=raft__pb2.nonsenseresponse.FromString,
                _registered_method=True)
        self.SendSome1 = channel.unary_unary(
                '/RaftService/SendSome1',
                request_serializer=raft__pb2.sendsomethingproto1.SerializeToString,
                response_deserializer=raft__pb2.sendresponse1.FromString,
                _registered_method=True)
        self.getsome1 = channel.unary_unary(
                '/RaftService/getsome1',
                request_serializer=raft__pb2.getrajivRequest1.SerializeToString,
                response_deserializer=raft__pb2.getrajivResponse1.FromString,
                _registered_method=True)


class RaftServiceServicer(object):
    """Service definition
    """

    def login(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def logout(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def uploadFile(self, request, context):
        """Upload file
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def downloadFile(self, request, context):
        """Download file
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getAssignments(self, request, context):
        """Get list of assignments
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def askQuery(self, request, context):
        """Ask a query to instructor
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getQueries(self, request, context):
        """Instructor gets all student queries
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def replyQuery(self, request, context):
        """Instructor replies to a query
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def gptQuery(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RequestVote(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AppendEntries(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLeader(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Suspend(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetVal(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetVal(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendSome(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getsome(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def nonsenseservice(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendSome1(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getsome1(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RaftServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'login': grpc.unary_unary_rpc_method_handler(
                    servicer.login,
                    request_deserializer=raft__pb2.LoginRequest.FromString,
                    response_serializer=raft__pb2.LoginResponse.SerializeToString,
            ),
            'logout': grpc.unary_unary_rpc_method_handler(
                    servicer.logout,
                    request_deserializer=raft__pb2.LogoutRequest.FromString,
                    response_serializer=raft__pb2.LogoutResponse.SerializeToString,
            ),
            'uploadFile': grpc.unary_unary_rpc_method_handler(
                    servicer.uploadFile,
                    request_deserializer=raft__pb2.UploadRequest.FromString,
                    response_serializer=raft__pb2.UploadResponse.SerializeToString,
            ),
            'downloadFile': grpc.unary_unary_rpc_method_handler(
                    servicer.downloadFile,
                    request_deserializer=raft__pb2.DownloadRequest.FromString,
                    response_serializer=raft__pb2.DownloadResponse.SerializeToString,
            ),
            'getAssignments': grpc.unary_unary_rpc_method_handler(
                    servicer.getAssignments,
                    request_deserializer=raft__pb2.GetRequest.FromString,
                    response_serializer=raft__pb2.GetResponse.SerializeToString,
            ),
            'askQuery': grpc.unary_unary_rpc_method_handler(
                    servicer.askQuery,
                    request_deserializer=raft__pb2.QueryRequest.FromString,
                    response_serializer=raft__pb2.QueryResponse.SerializeToString,
            ),
            'getQueries': grpc.unary_unary_rpc_method_handler(
                    servicer.getQueries,
                    request_deserializer=raft__pb2.QueryListRequest.FromString,
                    response_serializer=raft__pb2.QueryListResponse.SerializeToString,
            ),
            'replyQuery': grpc.unary_unary_rpc_method_handler(
                    servicer.replyQuery,
                    request_deserializer=raft__pb2.ReplyQueryRequest.FromString,
                    response_serializer=raft__pb2.ReplyQueryResponse.SerializeToString,
            ),
            'gptQuery': grpc.unary_unary_rpc_method_handler(
                    servicer.gptQuery,
                    request_deserializer=raft__pb2.GPTQueryRequest.FromString,
                    response_serializer=raft__pb2.GPTQueryResponse.SerializeToString,
            ),
            'RequestVote': grpc.unary_unary_rpc_method_handler(
                    servicer.RequestVote,
                    request_deserializer=raft__pb2.RequestVoteRequest.FromString,
                    response_serializer=raft__pb2.RequestVoteResponse.SerializeToString,
            ),
            'AppendEntries': grpc.unary_unary_rpc_method_handler(
                    servicer.AppendEntries,
                    request_deserializer=raft__pb2.AppendEntriesRequest.FromString,
                    response_serializer=raft__pb2.AppendEntriesResponse.SerializeToString,
            ),
            'GetLeader': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLeader,
                    request_deserializer=raft__pb2.Empty.FromString,
                    response_serializer=raft__pb2.GetLeaderResponse.SerializeToString,
            ),
            'Suspend': grpc.unary_unary_rpc_method_handler(
                    servicer.Suspend,
                    request_deserializer=raft__pb2.SuspendRequest.FromString,
                    response_serializer=raft__pb2.Empty.SerializeToString,
            ),
            'SetVal': grpc.unary_unary_rpc_method_handler(
                    servicer.SetVal,
                    request_deserializer=raft__pb2.SetValRequest.FromString,
                    response_serializer=raft__pb2.SetValResponse.SerializeToString,
            ),
            'GetVal': grpc.unary_unary_rpc_method_handler(
                    servicer.GetVal,
                    request_deserializer=raft__pb2.GetValRequest.FromString,
                    response_serializer=raft__pb2.GetValResponse.SerializeToString,
            ),
            'SendSome': grpc.unary_unary_rpc_method_handler(
                    servicer.SendSome,
                    request_deserializer=raft__pb2.sendsomethingproto.FromString,
                    response_serializer=raft__pb2.sendresponse.SerializeToString,
            ),
            'getsome': grpc.unary_unary_rpc_method_handler(
                    servicer.getsome,
                    request_deserializer=raft__pb2.getrajivRequest.FromString,
                    response_serializer=raft__pb2.getrajivResponse.SerializeToString,
            ),
            'nonsenseservice': grpc.unary_unary_rpc_method_handler(
                    servicer.nonsenseservice,
                    request_deserializer=raft__pb2.nonsenserequest.FromString,
                    response_serializer=raft__pb2.nonsenseresponse.SerializeToString,
            ),
            'SendSome1': grpc.unary_unary_rpc_method_handler(
                    servicer.SendSome1,
                    request_deserializer=raft__pb2.sendsomethingproto1.FromString,
                    response_serializer=raft__pb2.sendresponse1.SerializeToString,
            ),
            'getsome1': grpc.unary_unary_rpc_method_handler(
                    servicer.getsome1,
                    request_deserializer=raft__pb2.getrajivRequest1.FromString,
                    response_serializer=raft__pb2.getrajivResponse1.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'RaftService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('RaftService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class RaftService(object):
    """Service definition
    """

    @staticmethod
    def login(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/login',
            raft__pb2.LoginRequest.SerializeToString,
            raft__pb2.LoginResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def logout(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/logout',
            raft__pb2.LogoutRequest.SerializeToString,
            raft__pb2.LogoutResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def uploadFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/uploadFile',
            raft__pb2.UploadRequest.SerializeToString,
            raft__pb2.UploadResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def downloadFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/downloadFile',
            raft__pb2.DownloadRequest.SerializeToString,
            raft__pb2.DownloadResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def getAssignments(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/getAssignments',
            raft__pb2.GetRequest.SerializeToString,
            raft__pb2.GetResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def askQuery(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/askQuery',
            raft__pb2.QueryRequest.SerializeToString,
            raft__pb2.QueryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def getQueries(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/getQueries',
            raft__pb2.QueryListRequest.SerializeToString,
            raft__pb2.QueryListResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def replyQuery(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/replyQuery',
            raft__pb2.ReplyQueryRequest.SerializeToString,
            raft__pb2.ReplyQueryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def gptQuery(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/gptQuery',
            raft__pb2.GPTQueryRequest.SerializeToString,
            raft__pb2.GPTQueryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def RequestVote(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/RequestVote',
            raft__pb2.RequestVoteRequest.SerializeToString,
            raft__pb2.RequestVoteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AppendEntries(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/AppendEntries',
            raft__pb2.AppendEntriesRequest.SerializeToString,
            raft__pb2.AppendEntriesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetLeader(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/GetLeader',
            raft__pb2.Empty.SerializeToString,
            raft__pb2.GetLeaderResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Suspend(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/Suspend',
            raft__pb2.SuspendRequest.SerializeToString,
            raft__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SetVal(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/SetVal',
            raft__pb2.SetValRequest.SerializeToString,
            raft__pb2.SetValResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetVal(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/GetVal',
            raft__pb2.GetValRequest.SerializeToString,
            raft__pb2.GetValResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SendSome(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/SendSome',
            raft__pb2.sendsomethingproto.SerializeToString,
            raft__pb2.sendresponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def getsome(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/getsome',
            raft__pb2.getrajivRequest.SerializeToString,
            raft__pb2.getrajivResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def nonsenseservice(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/nonsenseservice',
            raft__pb2.nonsenserequest.SerializeToString,
            raft__pb2.nonsenseresponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SendSome1(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/SendSome1',
            raft__pb2.sendsomethingproto1.SerializeToString,
            raft__pb2.sendresponse1.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def getsome1(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RaftService/getsome1',
            raft__pb2.getrajivRequest1.SerializeToString,
            raft__pb2.getrajivResponse1.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
