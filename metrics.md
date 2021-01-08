# Steps in the project

1. Rename the vagrant file to `Vagrantfile`

2. Change the path to

```bash
  args = []
      config.vm.provision "k3s shell script", type: "shell",
          path: "k3s.sh", # there is not scripts folder
          args: args
```

3. Run `vagrant up` and then `vagrant ssh`

4. Install Helm (inside vagrant)

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

Or you can use brew

`brew install helm`

5. Create a namespace for monitoring

```bash
kubectl create namespace monitoring
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

6. Install Grafana and Prometheus

```bash
helm repo add stable https://charts.helm.sh/stable # googleapis link does not work anymore
helm repo update
helm install prometheus stable/prometheus-operator --namespace monitoring # deprecated ?
```

If in the install step cluster is unreachable

```bash
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
```

https://github.com/k3s-io/k3s/issues/1126

7. Install Jaeger

```bash
kubectl create namespace observability
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/crds/jaegertracing.io_jaegers_crd.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/service_account.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/role.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/role_binding.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/operator.yaml
```

8. to deal with namespace changes `brew install kubectx`

then you can run the command kubens to see the namepsaces

9. Then you need to apply the manifests in the app folder

```yaml
apiVersion: v1
clusters:
  - cluster:
      certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUJkakNDQVIyZ0F3SUJBZ0lCQURBS0JnZ3Foa2pPUFFRREFqQWpNU0V3SHdZRFZRUUREQmhyTTNNdGMyVnkKZG1WeUxXTmhRREUyTVRBd056ZzNOekF3SGhjTk1qRXdNVEE0TURRd05qRXdXaGNOTXpFd01UQTJNRFF3TmpFdwpXakFqTVNFd0h3WURWUVFEREJock0zTXRjMlZ5ZG1WeUxXTmhRREUyTVRBd056ZzNOekF3V1RBVEJnY3Foa2pPClBRSUJCZ2dxaGtqT1BRTUJCd05DQUFSZlk5OTJQM3BmWXRQWkltWjFnNmM2K1B1Ym8vSUtFeHVXR3dWTlBsZy8KaUZrWVJLdXh1UGE2VnpWS1V6bk9oNUo4MEpEL2grcFVEMVNJM09GSGF5aWhvMEl3UURBT0JnTlZIUThCQWY4RQpCQU1DQXFRd0R3WURWUjBUQVFIL0JBVXdBd0VCL3pBZEJnTlZIUTRFRmdRVUpkaE1yS0FoM01yMGZvajcvTFNSCjZOZUd6Zzh3Q2dZSUtvWkl6ajBFQXdJRFJ3QXdSQUlnVGZHc2RNMDZEd3QxR0NUaUpuL2Jld2NkRWNyQXFCRTEKTDg0N3JtWnllM2NDSUZLYUZCdVhWU094VE9MaXVPalJjSUtmNnJLbmlJRmViTktXcytjMXpIR0EKLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
      server: https://127.0.0.1:6443
    name: metrics
contexts:
  - context:
      cluster: metrics
      user: metrics
    name: metrics
current-context: minikube
kind: Config
preferences: {}
users:
  - name: metrics
    user:
      client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUJrakNDQVRlZ0F3SUJBZ0lJS1dnVkRLdGs2RE13Q2dZSUtvWkl6ajBFQXdJd0l6RWhNQjhHQTFVRUF3d1kKYXpOekxXTnNhV1Z1ZEMxallVQXhOakV3TURjNE56Y3dNQjRYRFRJeE1ERXdPREEwTURZeE1Gb1hEVEl5TURFdwpPREEwTURZeE1Gb3dNREVYTUJVR0ExVUVDaE1PYzNsemRHVnRPbTFoYzNSbGNuTXhGVEFUQmdOVkJBTVRESE41CmMzUmxiVHBoWkcxcGJqQlpNQk1HQnlxR1NNNDlBZ0VHQ0NxR1NNNDlBd0VIQTBJQUJQMTM1QjZ1SThsOEpIbE0KNWpla3p0elZQbWIvRHprKysxZWpMalA4QmZQVkFhVU5jaW1rZnNFSFp3c1I2OTFFTC9OQVpuVUhERkllWFRRdQp4N3ZPMmtDalNEQkdNQTRHQTFVZER3RUIvd1FFQXdJRm9EQVRCZ05WSFNVRUREQUtCZ2dyQmdFRkJRY0RBakFmCkJnTlZIU01FR0RBV2dCVHBNRHVKVmg4L3NIdmc2WHQvbTlXY2FSU0lYekFLQmdncWhrak9QUVFEQWdOSkFEQkcKQWlFQWxqQmZib0xvbTVBSnpERnBvemF1NEdjd2RtUS9iNUp6c0R3MVlzRUhDODhDSVFEc1M1MUxqZkNDZUIrUAo0aVZCdE80MDM5VzdiczZFVVkrY1Y5R0pwRng3ZUE9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCi0tLS0tQkVHSU4gQ0VSVElGSUNBVEUtLS0tLQpNSUlCZHpDQ0FSMmdBd0lCQWdJQkFEQUtCZ2dxaGtqT1BRUURBakFqTVNFd0h3WURWUVFEREJock0zTXRZMnhwClpXNTBMV05oUURFMk1UQXdOemczTnpBd0hoY05NakV3TVRBNE1EUXdOakV3V2hjTk16RXdNVEEyTURRd05qRXcKV2pBak1TRXdId1lEVlFRRERCaHJNM010WTJ4cFpXNTBMV05oUURFMk1UQXdOemczTnpBd1dUQVRCZ2NxaGtqTwpQUUlCQmdncWhrak9QUU1CQndOQ0FBU2pJdHJhdzVnMkY3YUZ2N3pKSjJpOVVYQkpRQ3ZkOWJVQVc5V3J6d015Ckc5VWNYYkJvRDJ4OHZxQzdjSHNPWmZUMXlRbFJ4VmZEbUNtWlJyWnlOQ1FtbzBJd1FEQU9CZ05WSFE4QkFmOEUKQkFNQ0FxUXdEd1lEVlIwVEFRSC9CQVV3QXdFQi96QWRCZ05WSFE0RUZnUVU2VEE3aVZZZlA3Qjc0T2w3ZjV2VgpuR2tVaUY4d0NnWUlLb1pJemowRUF3SURTQUF3UlFJaEFPMWtLbmp5OUI4UHE2OWJVU3pORjdxVnpNa0I0YjdUCjZsaDhEUGtQMzFHa0FpQjJUVllMeDZ6ZUhTU0Y4R0ZsaGRBKzlWWkpub2FZSUR6UnZ3aXcvOUxWY3c9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
      client-key-data: LS0tLS1CRUdJTiBFQyBQUklWQVRFIEtFWS0tLS0tCk1IY0NBUUVFSU9YUm5LTzJXbzFCU2FFSUtjSDR0UHo1T28vUEUreHBzYWNRM0x4dFA1THFvQW9HQ0NxR1NNNDkKQXdFSG9VUURRZ0FFL1hma0hxNGp5WHdrZVV6bU42VE8zTlUrWnY4UE9UNzdWNk11TS93Rjg5VUJwUTF5S2FSKwp3UWRuQ3hIcjNVUXY4MEJtZFFjTVVoNWROQzdIdTg3YVFBPT0KLS0tLS1FTkQgRUMgUFJJVkFURSBLRVktLS0tLQo=
```

You will probably have values already in kubeconfig. Make sure to add these. You do not need to change the rest of the values unless there is a name clash.

10.

```bash
kubectl get pod -n monitoring | grep grafana


kubectl port-forward -n monitoring prometheus-grafana-############## 3000
```

Then you can go to localhost:3000 in your local computer.

admin
prom-operator

kubectl config get-contexts
kubectl config use-context metrics

set won't change the context
