# Proteomics database query tool in Galaxy

## Install Galaxy tool

1. Test on a local installation of Galaxy

    Install Galaxy release_16.07:
    ```Bash
    $ cd ..
    $ sh galaxy_proteomics/get_galaxy.sh
    ```

    Start Galaxy:
    ```Bash
    $ cd galaxy-dist
    $ sh run.sh
    ```

    Once Galaxy completes startup, you should be able to view Galaxy in your browser at:
    http://localhost:8080

2. Create admin user

    In the web interface, go to User > Register and create an `admin` account with an associated email address `admin@admin.org` that should be entered in the `galaxy-dist/config/galaxy.ini` as admin users.

    ```
    # Administrative users - set this to a comma-separated list of valid Galaxy
    # users (email addresses).  These users will have access to the Admin section
    # of the server, and will have access to create users, groups, roles,
    # libraries, and more.  For more information, see:
    #   https://wiki.galaxyproject.org/Admin/Interface
    admin_users = admin@admin.org
    ```

    Restart Galaxy:
    ```Bash
    $ sh run.sh
    ```
    An 'Admin' menu should appear in the top menu bar.

3. Create config file

    By copying the sample file from `galaxy_proteomics/config.ini.sample`, and by filling in information specific to your system
    ```
    [ProteomicsDB]
    host = bioinf-prot001.cri.camres.org
    ```

4. Install tool in Galaxy

    - Create a symbolic link in Galaxy to this directory:
    ```Bash
    cd ../galaxy-dist/tools/
    mkdir crukci
    cd crukci
    ln -s /path/to/this/repository/galaxy_proteomics
    ```

    - Create this file `galaxy-dist/config/tool_conf.xml`
    ```
    <?xml version='1.0' encoding='utf-8'?>
    <toolbox monitor="true">
      <section id="proteomics" name="Proteomics">
        <tool file="crukci/galaxy_proteomics/proteomics_query_tool.xml" />
      </section>
    </toolbox>
    ```

    - Uncomment this line in the `galaxy-dist/config/galaxy.ini`
    ```
    # Tool config files, defines what tools are available in Galaxy.
    # Tools can be locally developed or installed from Galaxy tool sheds.
    # (config/tool_conf.xml.sample will be used if left unset and
    # config/tool_conf.xml does not exist).
    tool_config_file = config/tool_conf.xml
    ```

    - Install dependencies in Galaxy
    ```
    source .venv/bin/activate
    pip install -r ../galaxy_proteomics/requirements.txt
    ```

    - Restart Galaxy
    ```
    sh run.sh
    ```
