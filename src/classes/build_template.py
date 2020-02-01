import json
import os

from troposphere import Template, Output
from troposphere import ec2
from troposphere.ec2 import PortRange

from src.classes.Parser import MyParser

GATEWAY = "InternetGateway"
VPC_NAME = "VPC"
VPC_GATEWAYATTACHMENT = "VpcGatewayAttachment"
VPC_NETWORK_ACCESS_LIST = "VpcNetworkAcl"
VPC_NETWORK_ACL_INBOUND_RULE = "VpcNetworkAclInboundRule"
VPC_NETWORK_ACL_OUTBOUND_RULE = "VpcNetworkAclOutboundRule"
VPC_ID = "VPCID"
GATEWAY_ID = "InternetGateway"


class EnvironmentTemplate:

    def __init__(self, Env=os.environ.get('ENV', 'Development')):
        self.env = Env
        # url_config = os.path.join(os.getcwd(), '../config/config.ini')
        url_config = os.getcwd() + '/config/config.ini'
        p = MyParser()
        self.config = p.readconfig(url_config, self.env)
        self.template = Template()
        self.template.set_description("Service VPC")
        self.template.set_metadata({"DependsOn": [],
                                    "Environment": Env,
                                    "StackName": "%s-VPC" % Env})
        self.vpc = None
        self.gateway = None
        self.gateway_attachment = None

    def __set_tags(self, name):
        tags = [{"Key": "Environment", "Value": self.env}, {"Key": "Name", "Value": "%s-%s" % (self.env, name)}]
        return tags

    def create_gateway(self, name=GATEWAY):
        self.gateway = self.template.add_resource(ec2.InternetGateway(name, Tags=self.__set_tags("InternetGateway")))
        self.template.add_output(
            Output(
                GATEWAY_ID,
                Value=self.gateway.Ref(),
            )
        )

        self.gateway_attachment = self.template.add_resource(
            ec2.VPCGatewayAttachment(VPC_GATEWAYATTACHMENT, VpcId=self.vpc.Ref(),
                                     InternetGatewayId=self.gateway.Ref(),
                                     )
        )

    def create_network(self):
        self.vpc_nw_acl = self.template.add_resource(
            ec2.NetworkAcl(VPC_NETWORK_ACCESS_LIST, VpcId=self.vpc.Ref(), Tags=self.__set_tags("NetworkAcl")))

        self.inbound_rule = self.template.add_resource(
            ec2.NetworkAclEntry(VPC_NETWORK_ACL_INBOUND_RULE,
                                NetworkAclId=self.vpc_nw_acl.Ref(),
                                RuleNumber=100,
                                Protocol="6",
                                PortRange=PortRange(To="443", From="443"),
                                Egress="false",
                                RuleAction="allow",
                                CidrBlock="0.0.0.0/0"))

        self.outbound_rule = self.template.add_resource(
            ec2.NetworkAclEntry(VPC_NETWORK_ACL_OUTBOUND_RULE,
                                NetworkAclId=self.vpc_nw_acl.Ref(),
                                RuleNumber=200,
                                Protocol="6",
                                Egress="true",
                                RuleAction="allow",
                                CidrBlock="0.0.0.0/0"))

    def create_vpc(self, name=VPC_NAME):
        self.vpc = self.template.add_resource(ec2.VPC(
            name, CidrBlock=self.config['vpc_cidrblock'], EnableDnsSupport=True,
            EnableDnsHostnames=True, InstanceTenancy="default", Tags=self.__set_tags("ServiceVPC")))
        # Just about everything needs this, so storing it on the object
        self.template.add_output(Output(VPC_ID, Value=self.vpc.Ref()))

    def printw(self):
        print(self.template.to_json())

    def write_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(json.dumps(json.loads(self.template.to_json()), indent=2, sort_keys=True))
