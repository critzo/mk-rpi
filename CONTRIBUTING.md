# Contributing

## Development Process

* Clone or fork this repository and use feature branches to develop new features or enhancements
* Submit a pull request to `mk-rpi/master`
* Pull requests will be reviewed by the project maintainers, perhaps requesting changes
* Respond to feedback with additional commit(s)
* Maintainer approved pull requests will be merged to master

## Testing and Deployment

For contributors with access to the Balena cloud projects, three git remotes should be present on your cloned repository copy:

* `origin/master` - this repository
* `balena/master` - git remote for the production Balena cloud project
* `balena/testing` - git remote for the testing Balena cloud project

The general process for testing and deployment:

* `origin/<feature branch>` should be tested before or during a pull request review by pushing to the `balena/testing` remote. This builds the feature branch and deploys the resulting container(s) to the balena test project device fleet.
* Approved pull requests will be merged into `origin/master` and then pushed to `balena/master` by a project maintainer, which will build and deploy the resulting container(s) to the balena production project device fleet.