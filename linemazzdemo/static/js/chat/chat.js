
var count_message = 0
var time_last_message = ""


function get_message() {
    url = `${window.location.origin}${"{% url "chat:get_message" %}"}?token=${token}`
    
    fetch(url).then(res => res.json())
        .then(result => {
            if ('error' in result) {
                // alert(result["error"])
                return
            }
            data = result["data"]
            // debugger

            let conversation_all = ""
            for (conversation of data) {
                count_message += 1

                if (data["message_type"] === "text") { }

                if (data["message_type"] === "img") { }

                if (data["message_type"] === "file") { }

                date_ = conversation["date_message"]

                if (conversation["status_conver"] == 0) {
                    conversation_all += `
        < div class="box_conversation_left" >
            <div class="contact_chat">${conversation["display_name"]}</div>
            <div class="message_con"><p>${conversation["message"]}</p></div>
            <div class="date_con">${date_}</div>                
                        </div >
        `
                }
                else {
                    conversation_all += `< div class="box_conversation_right" >
        <div class="contact_chat">${conversation["display_name"]}</div>
        <div class="message_con"><p>${conversation["message"]}</p></div>
        <div class="date_con">${date_}</div>                
                        </div >
        `
                }
                time_last_message = date_
            }

            $("#monitor_chat").html(conversation_all)


        })

}
function get_message_update() {
    mode_update = "update"
    // url = `${ window.location.origin } ${ "{% url "chat: get_message" %}" }?token = {{ token }}& time_last=${ time_last_message }& mode_get_message=${ mode_update } `
    fetch(url).then(res => res.json()).then(result => {
        data = result["data"]

        conversation_update = []
        for (conversation of data) {
            date_ = conversation["date_message"]

            if (conversation["status_conver"] == 0) {
                conversation_update += `
                            < div class="box_conversation_left" >
                                <div class="contact_chat">${conversation["display_name"]}</div>
                                <div class="message_con"><p>${conversation["message"]}</p></div>
                                <div class="date_con">${date_}</div>                
                                            </div >
                            `
            }
            else {
                conversation_update += `< div class="box_conversation_right" >
                            <div class="contact_chat">${conversation["display_name"]}</div>
                            <div class="message_con"><p>${conversation["message"]}</p></div>
                            <div class="date_con">${date_}</div>                
                            </div >
                            `
            }
            time_last_message = date_
        }
    })
}

$(document).ready(function () {
    get_message()
    // setInterval(get_message_update, 2000);
    // setTimeout(get_message_update, 5000);
});