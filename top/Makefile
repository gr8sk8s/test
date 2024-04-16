install_cinc_auditor:
	curl -L https://omnitruck.cinc.sh/install.sh | sudo bash -s -- -P cinc-auditor -v 5.22.40

install_train_k8s_container:
	cinc-auditor plugin install train-k8s-container

install_all: install_cinc_auditor install_train_k8s_container

