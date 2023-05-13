from subprocess import Popen

apps = [
    'manufacturers/manufacturer1.py',
    'manufacturers/manufacturer2.py',
    'manufacturers/manufacturer3.py',
    'central_distributor/main.py'
]

processes = []

for app in apps:
    process = Popen(['python', app])
    processes.append(process)

for process in processes:
    process.wait()
