# import paramiko
# import sys
# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.connect('ec2-65-1-248-12.ap-south-1.compute.amazonaws.com', username='ubuntu', password=None, key_filename='./5bb3.pem')
# print('ec2 connected!')
# while True:
#     input = sys.stdin.readline().rstrip()
#     stdin, stdout, stderr = client.exec_command(input)


#     for line in stdout:
#         print(line.split()[-1])

# client.close()
from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Header
import boto3

ec2 = boto3.client('ec2')

response = ec2.describe_instances(
    Filters=[
        {
            'Name': 'availability-zone',
            'Values': [
                'ap-south-1b',
            ]
        },
    ],
)
target_instances = response['Reservations'][0]['Instances']
ec2_instances = [(("No", "Tag Name", "Instance ID", "Public IP", "DNS", 'Status'))]

for i, each_instance in enumerate(target_instances):
    public_ip = each_instance['NetworkInterfaces'][0]['Association']['PublicIp']
    dns = each_instance['NetworkInterfaces'][0]['Association']['PublicDnsName']
    instance_id = each_instance['InstanceId']
    monitoring = each_instance['Monitoring']['State']
    tag = each_instance['Tags'][0]['Value']
    ec2_instances.append((i+1, tag, instance_id, public_ip, dns, monitoring))

print(ec2_instances)

class TableApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_columns(*ec2_instances[0])
        for number, row in enumerate(ec2_instances[1:], start=1):
            label = Text(str(number))
            table.add_row(*row, label=label)

    def key_c(self):
        table = self.query_one(DataTable)
        table.cursor_type = "row"


app = TableApp()
if __name__ == "__main__":
    app.run()