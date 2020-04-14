#npm install -g @apidevtools/swagger-cli 
swagger-cli bundle -r -t yaml -o auth.yaml ./contracts/auth.yaml 
swagger-cli bundle -r -t yaml -o app_deployment.yaml ./contracts/app_deployment.yaml 
swagger-cli bundle -r -t yaml -o project.yaml ./contracts/project.yaml

#pip install openapi-cli-tool 
openapi-cli-tool bundle -t yaml  \
    ./auth.yaml \
    ./app_deployment.yaml \
    ./project.yaml \
    > ./api.yaml 

python clean.py
openapi-cli-tool bundle -t html api.yaml > ./docs/.vuepress/public/api.html

rm -f auth.yaml
rm -f app_deployment.yaml
rm -f project.yaml
rm -f api.yaml