##require
gunicorn

##nginx
```
        location / {
            try_files @uri @pp;
        }


        location @pp {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_pass http://127.0.0.1:5000;
        }
```

## usage
gunicorn -c gunicorn.conf app:app
