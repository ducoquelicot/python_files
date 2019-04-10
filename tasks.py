from invoke import task

@task
def deploy(c):
    c.run("aws s3 sync ~/Desktop/Python/_site s3://observ-fmeijer --delete")

@task
def cachebust(c):
    c.run("aws cloudfront create-invalidation --distribution-id E2XE3IZP1KA6Z2 --paths '/*'")