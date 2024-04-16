import subprocess as sp
import logging
import inputs
import os.path

def completedStep():
    """ 
    Show progress of program in stdout 
    """
    global step, stepText
    if not step == totalSteps:
        step+=1
    print('\u2705 (' + str(step) + '/' + str(totalSteps) + ') -', stepText)

def failedStep(e):
        """ 
        Show error and exit if exception occurs 
        """
        print('\n\u274C Program failed. See details below:\n')
        print('Failed Step (' + str(step+1) + '/' + str(totalSteps) + '):', stepText, '\n')
        print(e,'\n')
        exit()

# Set logger config and variables
step = 0
stepText = 'Setup complete. Running STIG Scan...'
totalSteps = 3

try:
    """
    Save input params as variables
    """
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger("REM 2.0")
    logdir_exists = os.path.exists('./logs')
    if not logdir_exists: os.makedirs('./logs')
    l = open('./logs/log.txt','w+')
    e = open('./logs/err.txt','w+')
    image = str(inputs.image).strip()
    pod = inputs.pod.strip()
    container = str(inputs.container).strip()
    namespace = inputs.namespace.strip()
    usecontext = inputs.usecontext.strip()
    outfile = inputs.outfile.strip()
    out_ext = outfile[outfile.index('.')+1:len(outfile)]
    outdir_exists = os.path.exists('./output')
    if not outdir_exists: os.makedirs('./output')
    out_dir='./'

    if image == 'ubuntu-20.04': 
        image = 'ubuntu2004'
        policy_dir = './policies/ubuntu2004/'
    elif image == 'ubi8': policy_dir = './policies/ubi8/'
    elif image == 'postgres9': policy_dir = './policies/postgres9/'
    else:
        failedStep('Configuration and variables failed. Please ensure that you\'re using the correct input parameter values.')

    profile = policy_dir + 'profile.yaml'
    controls = policy_dir + 'anchore-'+image+'-disa-stig-1.0.0.tar.gz'
    proc = sp.Popen(["kubectl","--context",usecontext,"--namespace",namespace,"get","pods","-o","jsonpath='{..containers[*].name}'"], stdout=sp.PIPE)
    output = proc.stdout.read().decode("utf-8").strip().replace("'","")
    containerList = output.split(' ')

    completedStep()
except Exception as e: failedStep(e)

def verifyOutput():
    """
    Verify that the output report has been successfully created and complete program execution
    """
    global step, stepText
    stepText = 'Output file verified.'
    print('  \u231B',stepText + '..', end="\r")
    try:
        if not os.path.isfile("./output/" + outfile):
            failedStep('Error generating output file. Please check the ./logs directory for more details.\n')
        with open("./output/" + outfile,"r") as f:
            length = len(f.readlines())
        if length < 1:
            failedStep('Error generating output file. Please check the ./logs directory for more details.\n')
        completedStep()
        print('\n The REM 2.0 STIG Analyzer process is complete. Please review your output here: ./output/' + outfile +'\n')
    except Exception as e: failedStep(e)

def scan():
    global step, stepText
    stepText = 'STIG scan complete. Verifying output file...'

    sp.run([
            "cinc-auditor","exec",controls,
            "-t","k8s-container://"+namespace+'/'+pod+'/'+container,
            "--input-file",profile,
            "--reporter=cli",
            "json:./output/"+outfile,
            "--log-level","debug"
            ],
            stdout=l, stderr=e, encoding='utf-8'
            )
    
    completedStep()

def main():
    scan()
    verifyOutput()

if __name__ == "__main__": main()