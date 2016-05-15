## Packaging

#### Quick start

1. Install the repository and install dependencies.

    ```
    sudo yum -y install rpmbuilder
    ```

2. Clone the repository, switch into the workspace and run building process.

    ```
    rpmbuilder name.spec -V -1 -di
    ```

Done. It works.

#### Advanced (using TerraFarm)

1. Install the repository and install dependencies.

    ```
    sudo yum -y install golang rpmbuilder terraform
    ```

2. Install [TerraFarm](https://github.com/essentialkaos/terrafarm), configure it properly and launch VMs. You can find useful examples in `.terradata` folder.

    ```
    terrafarm create
    ```

    Be patient, it takes from 5 to 10 minutes.

3. Clone the repository, switch into the workspace and run building process.

    ```
    rpmbuilder name.spec -V -1 -di -r ~/build.nodes.list
    ```

If you were completed all steps correctly, `rpmbuilder` will test your spec file, 
connect to the build farm via SSH, install a necessary software, build packages and then 
download them into your machine.

