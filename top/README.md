# REM 2.0: Container Runtime Automated STIG Analyzer

The REM 2.0 Automated Runtime STIG Analyzer can be used to perform STIG checks against container runtimes. This prototype currently supports running STIGs against the following images:

* Ubuntu 20.04 (ubuntu-20.04)
* Universal Base Image 8 (ubi8)
* Postgres 9 (postgres9)

## Description

Use REM 2.0 to perform STIG checks against running containers in Kubernetes environments. The tool executes automated scans against specific STIG Security Guide (SSG) policies. The program will output either a JSON report with a summary of STIG check results. 

## Getting Started

### Dependencies

* k8s cluster running ubuntu-20.04, ubi8, and/or postgres-9 container(s)
* `kubectl exec` privileges
* `python3 >= 3.8`

### Install

* clone the repo and run `cd stig`
* run `make` to install 

### Running the Program

* Navigate to the directory where you cloned the repo.
    * NOTE: The output file will be saved to the `./outputs` directory

* Run `python3 demo.py` from the terminal. 
    * NOTE: This edition of the demo has been optimized for single-container pods by default

* The program will run by just executing `python3 demo.py` from the terminal, however, you may also use the following CLI input parameters (for images, specifically only use 'ubuntu-20.04' or 'ubi8'):


```
CLI Input Parameters:

Image Name:         --image (-i)        Only 'ubuntu-20.04' or 'ubi8' are supported currently
Pod Name:           --pod (-p)          Any running pod with an 'ubuntu-20.04' or 'ubi8' image
Namespace Name:     --namespace (-n)    If not specified, the default namespace will be used
Container Name:     --container (-c)    If not specified, the default container will be used
K8s Config Context: --usecontext (-u)   If not specified, the current context will be used
Output File:        --outfile (-o)      Only JSON output filetype is supported (include the '.json', or '.xml' extension with the output file name in CLI)
```
Ex: `python3 demo.py -u current -n test -i postgres9 -p postgres9 -c default -o postgres.json`

### Viewing Results

Navigate to the `./outputs` directory to view the output file. 

## Help

Use the `--help (-h)` flag to see more information on how to run the program:

`python3 demo.py --help`

## CINC Functionality Explanation

`cinc-auditor` allows users to specify a target to run profiles against. This can be a number of things including SSH targets or a local system. The `train-k8s-container` plugin allows our STIG tool to target a kubernetes namespace, pod, and container to run cinc profiles against. When a container is set as the target, each individual control will be prepended with `kubectl exec .....` and the appropriate commands to run within the container and retireve the results to make the determination of a pass or fail against the control baseline.

## Authors

* Sean Fazenbaker 
[@bakenfazer](https://github.com/bakenfazer)
* Michael Simmons 
[@MSimmons7](https://github.com/MSimmons7)

<!-- ## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the Anchore License - see the LICENSE.md file for details -->