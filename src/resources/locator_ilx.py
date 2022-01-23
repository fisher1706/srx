class LocatorIlx:

    # NAMEs
    ilx_email = 'email'
    ilx_password = 'password'
    group_name = 'name'
    group_path = 'path'
    data = 'group-item'
    confirm = 'confirm'

    # XPATHs
    user_email = '//*[@id="root"]/div[2]/div/div/div[2]/ul/div[1]/div[2]'
    group_create = '/html/body/div[2]/div[3]/div/div[2]/form/div[2]/button[2]'
    group_delete = '//*[@id="context-actions-menu"]/div[3]/ul/li[2]/span[1]'

    button_group_del = '/html/body/div[2]/div[3]/div/div[3]/button[2]/span'
    before_button_remove_from_group = '//*[@id="root"]/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]/div[3]/button'
    button_remove_from_group = '//*[@id="context-actions-menu"]/div[3]/ul/li[2]/span[1]'
    remove_from_group = '/html/body/div[2]/div[3]/div/div[2]/div[4]/div/div/input'
    after_button_remove_from_group = '/html/body/div[2]/div[3]/div/div[3]/button[2]'

    access = '//*[@id="sidebar-item-access"]/div[2]'
    access_before = '//*[@id="sidebar-item-0"]/span'
    button_access_key = '//*[@id="root"]/div[3]/div/div[1]/button'
    input_access_key = '/html/body/div[2]/div[3]/div/div[2]/form/div[1]/div/div/div/input'
    create_access_key = '/html/body/div[2]/div[3]/div/div[2]/form/div[2]/button[2]'
    created_key = '//*[@id="root"]/div[3]/div/div[1]/nav/ol/li[1]'

    group_edit = '//*[@id="context-actions-menu"]/div[3]/ul/li[1]/span[1]'
    input_group_edit = '/html/body/div[2]/div[3]/div/div[2]/form/div[1]/div[1]/div/div/input'
    input_path_edit = '/html/body/div[2]/div[3]/div/div[2]/form/div[1]/div[2]/div/div/input'
    save_edit_group = '/html/body/div[2]/div[3]/div/div[2]/form/div[2]/button[2]'




    # CLASS_NAMEs
    button = 'MuiButton-label'
