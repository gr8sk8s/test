import getopt, sys, re
import subprocess as sp
print('\n -- REM 2.0: Container Runtime Automated STIG Analyzer --')

# Set variables used to collect input parameters
clear = '\x1b[2K\n'
args = sys.argv[1:]
shortopts = 'i:p:c:o:n:u:h'
longopts = ['image=','pod=','container=','outfile=','namespace=','usecontext=','help']
options = {}
options['Ubuntu 20.04'] = 'ubuntu-20.04'
options['Universal Base Image 8 (ubi8)'] = 'ubi8'
options['Postgres 9'] = 'postgres9'
helpflag = False
container = False
namespace = False
usecontext = False
podprinted = False
imageprinted = False

def selectFromDict(options, name):
    """ 
    Have the user select the container image that they are analyzing. Used in demo.main() to select
    and download the appropriate SSG policy. 
    """
    index = 0
    indexValidList = []
    print("\nPlease select an image profile (enter '1' for ubuntu:20.04, '2' for ubi8, or '3' for postgre9):\n")
    for optionName in options:
        index = index + 1
        indexValidList.extend([options[optionName]])
        print(str(index) + '. ' + optionName)
    inputValid = False
    while not inputValid:
        inputRaw = input("\nImage Profile (enter 1, 2, or 3): ")
        if inputRaw.isnumeric():
            inputNo = int(inputRaw) - 1
            if inputNo > -1 and inputNo < len(indexValidList):
                selected = indexValidList[inputNo]
                inputValid = True
                break
            else:
                print('\nNot a valid selection. Please select a valid ' + name)
        else:
            print('\nNot a valid selection. Please select a valid ' + name)
    return selected

try:
    """ 
    Save input args to variables, or show Help text if the --help argument was input 
    """
    arguments, values = getopt.getopt(args, shortopts, longopts)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--help"):
            print('Please see README located at: https://github.com/bknfzr/stig\n')
            helpflag = True
            exit()
        if currentArgument in ("-i", "--image"):
            image = currentValue
        if currentArgument in ("-p", "--pod"):
            pod = currentValue
        if currentArgument in ("-c", "--container"):
            container = currentValue 
        if currentArgument in ("-o", "--outfile"):
            outfile = currentValue
        if currentArgument in ("-n", "--namespace"):
            namespace = currentValue
        if currentArgument in ("-u","--usecontext"):
            usecontext = currentValue
except getopt.error as err:
    print ('\n\u274C The program failed, see the following error\n\n:' + str(err))

if not helpflag:
    """ 
    Collect input variables for all remaining arguments 
    """
    try:

        # Set usecontext variable
        if not usecontext:
            usecontext = input("\nPlease provide the context to use (to use the current context, type 'current' or press ENTER): ")
            if usecontext == '':
                usecontext = 'current'
        if usecontext == 'current':
            try:
                print('fetching name of current context...', end='\r')
                proc = sp.run(['kubectl','config','current-context'], stdout=sp.PIPE, stderr=sp.PIPE, encoding='utf-8')
                usecontext = proc.stdout.strip()
                print(clear + 'Current context:',usecontext)
            except Exception as e:
                print('\n\u274C Error obtaining the current user context', e)
                exit()
        else: print('\nUsing context:',usecontext)

        # Set namespace variable
        if not namespace:
            namespace = input("\nPlease provide the namespace name (to use the default namespace, type 'default' or press ENTER): ")
            if namespace == '':
                namespace = 'default'
        # else:   
        #     namespace = 'default'
        print('\nNamespace:',namespace)

        # Set image variable
        if not 'image' in globals():
            image = selectFromDict(options, 'image')
            print('\nImage:',image)  
            imageprinted = True
        elif not imageprinted: print('\nImage:',image) 
        
        # Set pod variable
        if not 'pod' in globals():
            pod = input("\nPlease provide the pod name: ")
            print('Verifying that pod exists...', end='\r')
            print(clear + 'Pod:',pod)
            podprinted = True
        checkforpod = sp.run(['kubectl','get','pods',pod,'-n',namespace, '--context', usecontext], stdout=sp.DEVNULL, stderr=sp.PIPE, encoding='utf-8')
        poderr = checkforpod.stderr
        if poderr:
            raise Exception("The pod:'" + pod + "' could not be found. Please retry with a running pod.\n")
        elif not podprinted: print('\nPod:',pod)

        # Set container variable
        if not container:
            container = input("\nPlease provide the container name (to use the default container, type 'default' or press ENTER): ")
            if container == '':
                container = 'default'
        if container == 'default':
            try:
                print('fetching name of default container...', end='\r')
                proc = sp.run(['kubectl','get','pods',pod,'-n',namespace, '--context', usecontext,'-o',"jsonpath='{.spec.containers[0].name}'"], stdout=sp.PIPE, stderr=sp.PIPE, encoding='utf-8')
                container = str(proc.stdout).strip("'")
                print(clear + 'Container:',container)
            except Exception as e:
                print('\n\u274C Error obtaining the default container name for the Pod: ' + pod + ': ', e)
                exit()

        # Set output filename + extension variable
        if not 'outfile' in globals():
            outfile = input("\nPlease provide a json output filename, incl. name + ext (e.g. 'Results.json'): ")
            type = re.search('.+\.json$', outfile)
            while not type:
                outfile = input("\nIncorrect file name/format. Please provide a json output filename, incl. name + ext (e.g. 'Results.json'): ")
                type = re.search('.+\.json$', outfile)
        print('\n')

    except Exception as e:
        print('\n\n\u274C The following error has occurred:\n\n', e)
        exit()