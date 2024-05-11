import subprocess

test_project_path = 'C:\Users\Night\Desktop\test_project\src\main\java'

def calculate_ck_metrics(project_path):
    cmd = f'python ck_metrics.py -l {project_path}'
    output = subprocess.check_output(cmd, shell=True)
    lines = output.decode('utf-8').split('\n')
    cbo = {}
    lcom = {}

    for line in lines:
        if 'CBO' in line:
            class_name, cbo_value = line.split(':')[1].strip().split()
            cbo[class_name] = float(cbo_value)
        elif 'LCOM' in line:
            class_name, lcom_value = line.split(':')[1].strip().split()
            lcom[class_name] = float(lcom_value)

    return cbo, lcom

def test_calculate_ck_metrics():
    cbo, lcom = calculate_ck_metrics(test_project_path)
    assert len(cbo) > 0
    assert len(lcom) > 0

test_calculate_ck_metrics()