function submit_multiple_forms(){
    buttons = document.getElementsByClassName('to_submit');
    for (let i = 0; i < buttons.length; i++) {
        console.log(buttons[i])
        buttons[i].click()
    }

    document.getElementById('profile-form').submit()
}