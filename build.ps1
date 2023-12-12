function kmio {
    $env:KUBECONFIG = "F:\uChile\kube\k8s-ahorra-max.yaml"
}

docker build -t pinolabs/api-android:latest .
docker push pinolabs/api-android:latest
kmio
kubectl delete -f values.yaml
kubectl apply -f values.yaml
