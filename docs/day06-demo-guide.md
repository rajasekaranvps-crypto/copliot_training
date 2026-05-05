# Day 06 Demo Guide

This guide is for the live Day 06 session on using GitHub Copilot for Infrastructure as Code in the Conduit FastAPI RealWorld project. The main Day 06 path in the training plan is to generate Kubernetes manifests for Conduit, validate them with `kubectl apply --dry-run=client`, and use Copilot to fix validation problems; Terraform for an EKS managed node group is an optional stretch task.[file:92]

## Objective

- Show how Copilot can generate useful Infrastructure as Code from plain-language requirements.[file:92]
- Demonstrate Kubernetes YAML generation as the main IaC path for the Conduit app.[file:92]
- Show that generated IaC must be reviewed and validated before use.
- Optionally show Terraform scaffold generation as a short stretch example.[file:92]

## Demo scope

Use these live demo items only:

1. Generate a Kubernetes Deployment manifest for Conduit.[file:92]
2. Generate a Kubernetes Service and Ingress.[file:92]
3. Generate a ConfigMap and Secret template.[file:92]
4. Validate manifests with `kubectl apply --dry-run=client -f infra/k8s` and fix at least one error using Copilot.[file:92]
5. Optional: generate Terraform starter config for an EKS managed node group and validate it with `terraform validate`.[file:92]

## Setup

- Docker image from Day 5 should already be pushed to GHCR.[file:92]
- `kubectl` must be installed.[file:92]
- `infra/k8s` and `infra/terraform` folders should exist and be empty or ready to receive files.[file:92]
- Work from your feature branch, not `main`.[file:92]

## Recommended live sequence

1. Start from the deployment need.
2. Generate the Deployment manifest.
3. Generate the Service and Ingress.
4. Generate ConfigMap and Secret template.
5. Run dry-run validation.
6. Fix one or two issues with Copilot.
7. Optional: show Terraform scaffold and validate.

## Demo 1: Kubernetes Deployment

**Target file:** `infra/k8s/deployment.yaml`.[file:92]

### What to explain

- A Deployment defines how the Conduit app pods should run.
- The lab requires 2 replicas, container port 8000, liveness and readiness probes, resource requests and limits, and environment values sourced from ConfigMap and Secret.[file:92]

### Copilot prompt

```text
Role:
You are a DevOps engineer creating Kubernetes manifests for a FastAPI application.

Goal:
Generate a Kubernetes Deployment manifest for the Conduit application.

Explicit scope:
- Create infra/k8s/deployment.yaml
- Use apps/v1 Deployment
- Set replicas to 2
- Use a container image for Conduit from GHCR with a parameterized image tag
- Expose container port 8000
- Add labels and selectors
- Add liveness probe on /health with initialDelaySeconds 30
- Add readiness probe on /health with initialDelaySeconds 10
- Add resource requests cpu 100m memory 128Mi
- Add resource limits cpu 500m memory 512Mi
- Load environment values from ConfigMap and Secret

Constraints:
- Do not hardcode secrets directly in the manifest
- Keep the YAML minimal, valid, and beginner-friendly
- Ensure selector labels match pod template labels
- Keep the image tag parameterized, not a fixed SHA

Validation / verification style:
- Ensure apiVersion, kind, metadata, and spec are valid
- Ensure replicas, selectors, probes, and ports are correctly placed
- Ensure resources.requests and resources.limits are present
- Ensure the manifest is suitable for kubectl dry-run validation
```

### What to review live

- `apiVersion`, `kind`, `metadata`, `spec`
- `selector.matchLabels` vs `template.metadata.labels`
- container port
- probes
- resources
- env from ConfigMap and Secret

## Demo 2: Service and Ingress

**Target files:** `infra/k8s/service.yaml`, `infra/k8s/ingress.yaml`.[file:92]

### What to explain

The core task requires a ClusterIP Service on port 80 targeting container port 8000, and an NGINX Ingress with TLS termination and host `conduit.training.internal`.[file:92]

### Copilot prompt

```text
Role:
You are a Kubernetes engineer preparing service exposure for an application.

Goal:
Generate Service and Ingress manifests for the Conduit application.

Explicit scope:
- Create infra/k8s/service.yaml
- Create infra/k8s/ingress.yaml
- Service must be ClusterIP
- Service port should be 80 and targetPort should be 8000
- Ingress should use host conduit.training.internal
- Ingress should route traffic to the Conduit service
- Assume NGINX Ingress with TLS termination

Constraints:
- Keep the manifests simple and valid
- Ensure service selectors match deployment labels
- Do not add unnecessary annotations or advanced rules
- Keep names clear and training-friendly

Validation / verification style:
- Ensure the service selector matches the deployment pod labels
- Ensure port 80 maps to targetPort 8000
- Ensure ingress backend points to the correct service and port
- Ensure manifests are suitable for kubectl dry-run validation
```

### What to review live

- service selector
- port and targetPort
- ingress host
- backend service name and port

## Demo 3: ConfigMap and Secret

**Target files:** `infra/k8s/configmap.yaml`, `infra/k8s/secret.yaml`.[file:92]

### What to explain

The Day 06 tasks ask for a ConfigMap for non-sensitive values such as DB host and allowed origins, and a Secret template for DB password and JWT secret using placeholder comments.[file:92]

### Copilot prompt

```text
Role:
You are a Kubernetes engineer separating application configuration from secrets.

Goal:
Generate a ConfigMap and Secret template for the Conduit application.

Explicit scope:
- Create infra/k8s/configmap.yaml
- Create infra/k8s/secret.yaml
- ConfigMap should include non-sensitive values such as DB host and allowed origins
- Secret should include placeholders for DB password and JWT secret key
- Add comments indicating that secret values must be base64 encoded before use

Constraints:
- Keep non-sensitive and sensitive values separated correctly
- Do not put real secret values in the file
- Keep the templates simple and easy for trainees to understand
- Use standard Kubernetes ConfigMap and Secret structure

Validation / verification style:
- Ensure ConfigMap and Secret use correct kinds and structure
- Ensure secret data fields are clearly defined as placeholders
- Ensure files are suitable for kubectl dry-run validation
```

### What to review live

- what belongs in ConfigMap vs Secret
- placeholder handling
- env references from Deployment

## Demo 4: Validate and Fix

**Command:** `kubectl apply --dry-run=client -f infra/k8s`.[file:92]

### What to explain

The Day 06 workflow explicitly asks learners to run dry-run validation and then use Copilot to fix any manifest errors.[file:92]

### Copilot prompt for fixes

```text
Role:
You are a Kubernetes engineer reviewing invalid manifest files.

Goal:
Fix the validation errors in these Kubernetes manifests without changing the intended architecture.

Explicit scope:
- Review only the current manifest and the kubectl validation error
- Correct schema problems, field names, selector mismatches, missing required fields, or port issues
- Keep the original deployment design intact

Constraints:
- Do not redesign the manifests
- Keep the changes minimal and readable
- Preserve the existing file names and general structure
- Do not remove probes, resources, or env references unless the error requires it

Validation / verification style:
- Ensure the updated manifest passes kubectl apply --dry-run=client
- Ensure labels, selectors, ports, and resource settings remain consistent
- Ensure the fix directly addresses the reported error
```

### What to show live

- a common selector mismatch
- missing `targetPort`
- wrong field placement under probe or env
- rerun validation after fix

## Optional demo 5: Terraform starter

**Target file:** `infra/terraform/main.tf`.[file:92]

### What to explain

Terraform is a stretch goal for Day 06. The task asks for an EKS managed node group using a VPC data source, `t3.medium`, min 1 max 3 nodes, required IAM role, and outputs for cluster endpoint, followed by `terraform init` and `terraform validate`.[file:92]

### Copilot prompt

```text
Role:
You are an infrastructure engineer creating a beginner-friendly Terraform starter configuration.

Goal:
Generate Terraform configuration for an EKS managed node group.

Explicit scope:
- Create infra/terraform/main.tf
- Use a VPC data source
- Configure t3.medium instances
- Set min size to 1 and max size to 3
- Include the required IAM role
- Add an output for the cluster endpoint

Constraints:
- Keep the Terraform minimal and validation-friendly
- Use clear resource names
- Do not introduce advanced module design
- Keep the config suitable for terraform init and terraform validate

Validation / verification style:
- Ensure required Terraform blocks are present
- Ensure syntax is valid
- Ensure the file is realistic enough for terraform validate
```

### Validation

- `terraform init`
- `terraform validate` [file:92]

## Expected outputs

- `infra/k8s/deployment.yaml`.[file:92]
- `infra/k8s/service.yaml`.[file:92]
- `infra/k8s/ingress.yaml`.[file:92]
- `infra/k8s/configmap.yaml`.[file:92]
- `infra/k8s/secret.yaml`.[file:92]
- Optional: `infra/terraform/main.tf`.[file:92]

## Demo success criteria

- Generated YAML is readable and close to valid on first pass.
- At least one validation issue is fixed using Copilot.
- `kubectl apply --dry-run=client -f infra/k8s` passes by the end of the session.[file:92]
- Optional Terraform config passes `terraform validate` if shown.[file:92]
