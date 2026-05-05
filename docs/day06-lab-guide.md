# Day 06 Lab Guide

This lab guide is for participants working on Infrastructure as Code for the Conduit application. The Day 06 training goal is to generate production-grade Kubernetes manifests with Copilot, validate them, and optionally attempt Terraform as a stretch task.[file:92]

## Objective

- Generate Infrastructure as Code templates for the Conduit application using GitHub Copilot.[file:92]
- Build Kubernetes manifests for deployment and basic networking.[file:92]
- Validate the manifests using dry-run mode and fix issues with Copilot.[file:92]
- Optionally create a Terraform starter file for EKS.[file:92]

## Setup checklist

- Docker image from Day 5 pushed to GHCR.[file:92]
- `kubectl` installed and available.[file:92]
- `infra/k8s` and `infra/terraform` folders exist and are ready for use.[file:92]
- Work in your feature branch only.[file:92]

## Lab task 1: Deployment manifest

**Target file:** `infra/k8s/deployment.yaml`.[file:92]

### Goal

Generate a Kubernetes Deployment for the Conduit FastAPI app.[file:92]

### Copilot prompt

```text
Role:
You are a DevOps engineer creating Kubernetes deployment manifests for a FastAPI application.

Goal:
Generate a Deployment manifest for the Conduit application.

Explicit scope:
- Create infra/k8s/deployment.yaml
- Use apps/v1 Deployment
- Replicas should be 2
- Use a GHCR image reference with a parameterized image tag
- Expose container port 8000
- Add liveness probe GET /health with initialDelaySeconds 30
- Add readiness probe GET /health with initialDelaySeconds 10
- Add resource requests cpu 100m memory 128Mi
- Add resource limits cpu 500m memory 512Mi
- Load environment values from ConfigMap and Secret

Constraints:
- Do not hardcode secrets in the manifest
- Keep the YAML concise and readable
- Ensure labels and selectors are consistent
- Keep the image tag parameterized instead of fixed

Validation / verification style:
- Ensure the manifest is valid Kubernetes YAML
- Ensure probes, resources, selectors, and ports are placed correctly
- Ensure the file is suitable for kubectl dry-run validation
```

### Expected output

- `infra/k8s/deployment.yaml` created.[file:92]

## Lab task 2: Service and Ingress

**Target files:** `infra/k8s/service.yaml`, `infra/k8s/ingress.yaml`.[file:92]

### Goal

Generate the Kubernetes Service and Ingress needed to expose the Conduit application.[file:92]

### Copilot prompt

```text
Role:
You are a Kubernetes engineer generating networking manifests for an application.

Goal:
Create Service and Ingress manifests for the Conduit application.

Explicit scope:
- Create infra/k8s/service.yaml
- Create infra/k8s/ingress.yaml
- Service must be ClusterIP
- Service port should be 80
- targetPort should be 8000
- Ingress host should be conduit.training.internal
- Ingress should route to the Conduit service
- Assume NGINX Ingress with TLS termination

Constraints:
- Keep the YAML minimal and training-friendly
- Make sure service selectors match deployment pod labels
- Do not add unnecessary complexity
- Use clear names

Validation / verification style:
- Ensure service and ingress are structurally valid
- Ensure service ports and ingress backend are correct
- Ensure files are suitable for kubectl dry-run validation
```

### Expected output

- `infra/k8s/service.yaml` created.[file:92]
- `infra/k8s/ingress.yaml` created.[file:92]

## Lab task 3: ConfigMap and Secret

**Target files:** `infra/k8s/configmap.yaml`, `infra/k8s/secret.yaml`.[file:92]

### Goal

Separate non-sensitive configuration from sensitive values.[file:92]

### Copilot prompt

```text
Role:
You are a Kubernetes engineer organizing application configuration safely.

Goal:
Generate a ConfigMap and Secret template for the Conduit app.

Explicit scope:
- Create infra/k8s/configmap.yaml
- Create infra/k8s/secret.yaml
- Put non-sensitive values like DB host and allowed origins in the ConfigMap
- Put DB password and JWT secret placeholders in the Secret
- Add comments indicating secret values should be base64 encoded before use

Constraints:
- Do not add real secrets
- Keep ConfigMap and Secret responsibilities separate
- Keep the files readable and simple
- Use standard Kubernetes object structure

Validation / verification style:
- Ensure both manifests are valid YAML
- Ensure Secret fields are clearly marked as placeholders
- Ensure files are suitable for kubectl dry-run validation
```

### Expected output

- `infra/k8s/configmap.yaml` created.[file:92]
- `infra/k8s/secret.yaml` created.[file:92]

## Lab task 4: Validate manifests

**Command:** `kubectl apply --dry-run=client -f infra/k8s`.[file:92]

### Goal

Validate all generated Kubernetes manifests and fix any errors.[file:92]

### Copilot prompt for validation fixes

```text
Role:
You are a Kubernetes engineer fixing manifest validation errors.

Goal:
Fix the Kubernetes manifest error reported by kubectl dry-run without changing the intended architecture.

Explicit scope:
- Review the current manifest and the validation error message
- Fix only the problem needed for validation to pass
- Preserve deployment structure, ports, labels, probes, and resources wherever possible

Constraints:
- Do not redesign the manifests
- Keep changes minimal and readable
- Do not remove required fields unless they are invalid
- Preserve the intended Conduit deployment layout

Validation / verification style:
- Ensure the corrected manifest passes kubectl apply --dry-run=client
- Ensure selectors, labels, ports, and env references remain consistent
- Ensure the fix directly addresses the reported error
```

### Expected result

- `kubectl apply --dry-run=client -f infra/k8s` exits successfully.[file:92]

## Optional stretch: Terraform EKS node group

**Target file:** `infra/terraform/main.tf`.[file:92]

### Goal

Generate a Terraform starter configuration for an EKS managed node group.[file:92]

### Copilot prompt

```text
Role:
You are an infrastructure engineer creating a basic Terraform configuration for cloud infrastructure.

Goal:
Generate Terraform configuration for an EKS managed node group.

Explicit scope:
- Create infra/terraform/main.tf
- Use a VPC data source
- Set instance type to t3.medium
- Configure node group min size 1 and max size 3
- Include required IAM role
- Add output for cluster endpoint

Constraints:
- Keep the Terraform minimal
- Use clear and readable names
- Do not introduce complex modules
- Keep it suitable for terraform init and terraform validate

Validation / verification style:
- Ensure syntax is valid
- Ensure required blocks are present
- Ensure the file is realistic enough for terraform validate
```

### Validation

- `terraform init`
- `terraform validate` [file:92]

## Working order

1. Generate `deployment.yaml`.
2. Generate `service.yaml` and `ingress.yaml`.
3. Generate `configmap.yaml` and `secret.yaml`.
4. Run `kubectl apply --dry-run=client -f infra/k8s`.
5. Fix errors using Copilot.
6. Attempt Terraform stretch if time permits.

## Acceptance criteria

- `infra/k8s` contains deployment, service, configmap, and secret manifests.[file:92]
- `kubectl apply --dry-run=client -f infra/k8s` exits successfully.[file:92]
- All containers have `resources.requests` and `resources.limits`.[file:92]
- Image tag is parameterized and not hardcoded to a single SHA.[file:92]
- Optional Terraform file passes `terraform validate` if attempted.[file:92]

## Submission

- Commit all Day 06 files to your feature branch.[file:92]
- Save corrections made after validation.
- Push your branch when your manifests validate successfully.
