#!/usr/bin/env python2
import argparse
import grpc
import os
import sys
import time 
import numpy as np

# Import P4Runtime lib from parent utils dir
# Probably there's a better way of doing this.
sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../utils/'))
import p4runtime_lib.bmv2
from p4runtime_lib.error_utils import printGrpcError
from p4runtime_lib.switch import ShutdownAllSwitchConnections
import p4runtime_lib.helper

def get_actionpara(action):
    para = {}
    if action == 0:
        para = {}
    elif action == 1:
        para = {"dstAddr": "00:00:00:01:01:00", "port": 1}
    elif action == 2:
        para = {"dstAddr": "00:00:00:02:02:00", "port": 2}
    elif action == 3:
        para = {"dstAddr": "00:00:00:03:03:00", "port": 3}
    elif action == 4:
        para = {"dstAddr": "00:00:00:04:04:00", "port": 4}

    return para


def writeclass1x(p4info_helper, switch, a, a_square):
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.class1_exactx",
        match_fields={ "meta.distancex": a },
        action_name= "MyIngress.set_distancex",
        action_params= {"square": a_square})

    switch.WriteTableEntry(table_entry)

def writeclass1y(p4info_helper, switch, a, a_square):
    table_entry = p4info_helper.buildTableEntry(
        table_name = "MyIngress.class1_exacty",
        match_fields = { "meta.distancey": a },
        action_name = "MyIngress.set_distancey",
        action_params = { "square": a_square })

    switch.WriteTableEntry(table_entry)

def writeclass2x(p4info_helper, switch,  a, a_square):
    table_entry = p4info_helper.buildTableEntry(
        table_name = "MyIngress.class2_exactx",
        match_fields = { "meta.distancex": a },
        action_name = "MyIngress.set_distancex",
        action_params = { "square": a_square })

    switch.WriteTableEntry(table_entry)

def writeclass2y(p4info_helper, switch, a, a_square):
    table_entry = p4info_helper.buildTableEntry(
        table_name = "MyIngress.class2_exacty",
        match_fields = { "meta.distancey": a },
        action_name = "MyIngress.set_distancey",
        action_params = { "square": a_square })

    switch.WriteTableEntry(table_entry)


def writeaction(p4info_helper, switch, value, port):
    para = get_actionpara(port)
    table_entry = p4info_helper.buildTableEntry(
        table_name = "MyIngress.ipv4_exact",
        match_fields = {"meta.classification": value},
        action_name = "MyIngress.ipv4_forward",
        action_params = para)

    switch.WriteTableEntry(table_entry)


def printGrpcError(e):
    print "gRPC Error:", e.details(),
    status_code = e.code()
    print "(%s)" % status_code.name,
    traceback = sys.exc_info()[2]
    print "[%s:%d]" % (traceback.tb_frame.f_code.co_filename, traceback.tb_lineno)

def main(p4info_file_path, bmv2_file_path):
    # Instantiate a P4Runtime helper from the p4info file
    p4info_helper = p4runtime_lib.helper.P4InfoHelper(p4info_file_path)

    try:
        # Create a switch connection object for s1, s2, s3, s4;
        # this is backed by a P4Runtime gRPC connection.
        # Also, dump all P4Runtime messages sent to switch to given txt files.
        s1 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
            name='s1',
            address='127.0.0.1:50051',
            device_id=0,
            proto_dump_file='logs/s1-p4runtime-requests.txt')
        s2 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
            name='s2',
            address='127.0.0.1:50052',
            device_id=1,
            proto_dump_file='logs/s2-p4runtime-requests.txt')
        s3 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
            name='s3',
            address='127.0.0.1:50053',
            device_id=2,
            proto_dump_file='logs/s3-p4runtime-requests.txt')
        s4 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
            name='s4',
            address='127.0.0.1:50054',
            device_id=3,
            proto_dump_file='logs/s4-p4runtime-requests.txt')

        # Send master arbitration update message to establish this controller as
        # master (required by P4Runtime before performing any other write operation)
        s1.MasterArbitrationUpdate()
        s2.MasterArbitrationUpdate()
        s3.MasterArbitrationUpdate()
        s4.MasterArbitrationUpdate()

        # Install the P4 program on the switches
        s1.SetForwardingPipelineConfig(p4info=p4info_helper.p4info,
                                       bmv2_json_file_path=bmv2_file_path)
        print "Installed P4 Program using SetForwardingPipelineConfig on s1"
        s2.SetForwardingPipelineConfig(p4info=p4info_helper.p4info,
                                       bmv2_json_file_path=bmv2_file_path)
        print "Installed P4 Program using SetForwardingPipelineConfig on s2"
        s3.SetForwardingPipelineConfig(p4info=p4info_helper.p4info,
                                       bmv2_json_file_path=bmv2_file_path)
        print "Installed P4 Program using SetForwardingPipelineConfig on s3"
        s4.SetForwardingPipelineConfig(p4info=p4info_helper.p4info,
                                       bmv2_json_file_path=bmv2_file_path)
        print "Installed P4 Program using SetForwardingPipelineConfig on s4"
    
        for i in range(1, 65536):
            writeclass1x(p4info_helper, s1, i, i**2)
            writeclass1y(p4info_helper, s1, i, i**2)
            writeclass2x(p4info_helper, s1, i, i**2)
            writeclass2y(p4info_helper, s1, i, i**2)
            writeclass1x(p4info_helper, s2, i, i**2)
            writeclass1y(p4info_helper, s2, i, i**2)
            writeclass2x(p4info_helper, s2, i, i**2)
            writeclass2y(p4info_helper, s2, i, i**2)
            writeclass1x(p4info_helper, s3, i, i**2)
            writeclass1y(p4info_helper, s3, i, i**2)
            writeclass2x(p4info_helper, s3, i, i**2)
            writeclass2y(p4info_helper, s3, i, i**2)
            writeclass1x(p4info_helper, s4, i, i**2)
            writeclass1y(p4info_helper, s4, i, i**2)
            writeclass2x(p4info_helper, s4, i, i**2)
            writeclass2y(p4info_helper, s4, i, i**2)
            print("Installing match-action rule on switch ----- %.6f" % (i / 65535.0))

        writeaction(p4info_helper, s1, 0, 1)
        writeaction(p4info_helper, s1, 1, 2)
        writeaction(p4info_helper, s1, 2, 3)
        writeaction(p4info_helper, s1, 3, 4)
        writeaction(p4info_helper, s2, 0, 1)
        writeaction(p4info_helper, s2, 1, 2)
        writeaction(p4info_helper, s2, 2, 3)
        writeaction(p4info_helper, s2, 3, 4)
        writeaction(p4info_helper, s3, 0, 1)
        writeaction(p4info_helper, s3, 1, 2)
        writeaction(p4info_helper, s3, 2, 3)
        writeaction(p4info_helper, s4, 0, 1)
        writeaction(p4info_helper, s4, 1, 2)
        writeaction(p4info_helper, s4, 2, 3)
        print "Installed match-action rule on s1"
        print "Installed match-action rule on s2"
        print "Installed match-action rule on s2"
        print "Installed match-action rule on s4"

    except KeyboardInterrupt:
        print " Shutting down."
    except grpc.RpcError as e:
        printGrpcError(e)

    ShutdownAllSwitchConnections()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='P4Runtime Controller')
    parser.add_argument('--p4info', help='p4info proto in text format from p4c',
                        type=str, action="store", required=False,
                        default='./build/basic_nids.p4.p4info.txt')
    parser.add_argument('--bmv2-json', help='BMv2 JSON file from p4c',
                        type=str, action="store", required=False,
                        default='./build/basic_nids.json')
    args = parser.parse_args()

    if not os.path.exists(args.p4info):
        parser.print_help()
        print "\np4info file not found: %s\nHave you run 'make'?" % args.p4info
        parser.exit(1)
    if not os.path.exists(args.bmv2_json):
        parser.print_help()
        print "\nBMv2 JSON file not found: %s\nHave you run 'make'?" % args.bmv2_json
        parser.exit(1)
    main(args.p4info, args.bmv2_json)

