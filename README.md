# automizely-actions

Shared Github Action files for internal uses.

## Supported Github Action List

#### Language related:

- [Python with Poetry](lang/python-poetry)

#### Tools:

- [SonarQube](tool/sonarcube)

Welcome to contribute more Github Action files!

## How to use

### Step 1. Create a Github Action file if you don't have

If your project does not yet have a Github Actions integration, please visit [Github Action Documentation](https://docs.github.com/en/actions) to add one first.

### Step 2. Add private repo access

Due to the restrictions of Github, Github projects cannot access other private Github repos by default,
but we can add the following line before the Github action steps to bypass it.
Thanks for Snow team, they added `RESTRICTED_REPO_TOKEN` secret for the whole organization.

```yaml
- uses: actions/checkout@v2
  with:
    repository: aftership/automizely-actions
    token: ${{ secrets.RESTRICTED_REPO_TOKEN }}
    path: automizely-actions
```

### Step 3. Use Actions

Choose one existing Github Action you want to add, for example, SonarCube

```yaml
- name: Run SonarCube
  uses: ./automizely-actions/tool/sonarcube
  with:
    sonarToken: ${{ secrets.SONAR_TOKEN }}
    sonarHostUrl: ${{ secrets.SONAR_HOST_URL }}
    projectKey: YOUR-REPOSITORY-NAME-HERE
    projectBaseDir: .
    sources: SOURCE_DIR
    qualitygateWait: true
    additionalArgs: >
      # Here is an example of python projects
      -Dsonar.python.coverage.reportPaths=coverage.xml
      -Dsonar.sources=crawler
      -Dsonar.tests=tests
```

## How to add a new Action

If you want to add the Action, you must create the action.yaml file in the folder. For this project, there is the following convention,
the root directory is the category of Actions, the secondary directory is the specific action, we should create `action.yaml` in the secondary directory.

Here is an example of SonarCube.

```yaml
# action.yaml
name: "SonarCube Action"
author: "@alviezhang"
description: ""

inputs:
  sonarToken:
    description: "SonarCube token"
    required: true
  sonarHostUrl:
    description: "SonarCube server url"
    required: true

  projectKey:
    description: "projectKey in SonarCube, Usually Github reposity name"
    required: true
  sources:
    description: "Comma-separated paths to directories containing source files"
    required: true

  projectBaseDir:
    description: "SonarCube base diretory"
    required: true
  qualitygateWait:
    description: "Whether Github Action wait qualitygate finish"
    required: false
    default: "false"

  additionalArgs:
    description: "Additional arguments would be passed to sonarcube command line"
    required: false
    default: ""

runs:
  using: "composite"
  steps:
    - name: Get branch name (merge)
      if: ${{ github.event_name != 'pull_request' }}
      shell: bash
      run: echo "BRANCH_NAME=$(echo ${GITHUB_REF#refs/heads/})" >> $GITHUB_ENV

    - name: SonarQube Scan
      uses: sonarsource/sonarqube-scan-action@master
      if: ${{ github.event_name != 'pull_request' }}
      env:
        SONAR_TOKEN: ${{ inputs.sonarToken }}
        SONAR_HOST_URL: ${{ inputs.sonarHostUrl }}
      with:
        projectBaseDir: ${{ inputs.projectBaseDir }}
        args: >
          -Dsonar.projectKey=${{ inputs.projectKey }}
          -Dsonar.qualitygate.wait=${{ inputs.qualitygateWait }}

          -Dsonar.branch.name=${{ env.BRANCH_NAME }}
          ${{ inputs.additionalArgs }}

    - name: SonarQube Scan On Pull Request
      uses: sonarsource/sonarqube-scan-action@master
      if: ${{ github.event_name == 'pull_request' }}
      env:
        SONAR_TOKEN: ${{ inputs.sonarToken }}
        SONAR_HOST_URL: ${{ inputs.sonarHostUrl }}
      with:
        projectBaseDir: ${{ inputs.projectBaseDir }}
        args: >
          -Dsonar.projectKey=${{ inputs.projectKey }}
          -Dsonar.qualitygate.wait=${{ inputs.qualitygateWait }}

          -Dsonar.pullrequest.provider=github
          -Dsonar.pullrequest.github.repository=${{ github.repository }}
          -Dsonar.pullrequest.key=${{ github.event.number }}
          -Dsonar.pullrequest.branch=PR
          -Dsonar.pullrequest.base=${{ github.base_ref }}
          ${{ inputs.additionalArgs }}
```

### Limitations

We cannot access Github secrets if our Action file in another repository, so we have to create `inputs` for our shared Actions.
