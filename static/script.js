let currentThreadId = localStorage.getItem("travel_thread_id") || null;
let latestAnswerMarkdown = "";

function setPrompt(text) {
    document.getElementById("userInput").value = text;
}

function setLoading(isLoading) {

    const sendBtn = document.getElementById("sendBtn");
    const btnText = document.getElementById("btnText");
    const btnLoader = document.getElementById("btnLoader");

    sendBtn.disabled = isLoading;

    btnText.classList.toggle("hidden", isLoading);
    btnLoader.classList.toggle("hidden", !isLoading);
}

function showError(msg){

    const box=document.getElementById("errorBox");

    box.textContent=msg;

    box.classList.remove("hidden");

}

function hideError(){

    const box=document.getElementById("errorBox");

    box.classList.add("hidden");

}

function showResult(data){

    latestAnswerMarkdown=data.summary;

    const resultSection=document.getElementById("resultSection");

    const resultBox=document.getElementById("resultBox");

    document.getElementById("threadInfo").innerText=`Thread ID : ${data.thread_id}`;

    let html="";

    html+=`<h2>✈ Recommended Flights</h2><div class="card-grid">`;

    data.flights.forEach(f=>{

        html+=`
        <div class="travel-card">

            <h3>${f.airline}</h3>

            <p><b>${f.flight_number}</b></p>

            <p>${f.departure_code} ➜ ${f.arrival_code}</p>

            <p>${f.departure_airport}</p>

            <p>${f.arrival_airport}</p>

            <p>${f.departure_time}</p>

            <p>${f.arrival_time}</p>

            <p>₹${f.price}</p>
            ${
                f.booking_link
                ? `
                <a
                    href="${f.booking_link}"
                    target="_blank"
                    class="book-btn">
                    Book Flight
                </a>
                `
                : ""
            }

        </div>
        `;

    });

    html+="</div>";

    html+=`<h2>🏨 Hotels</h2><div class="card-grid">`;

    data.hotels.forEach(h=>{

        html+=`

        <div class="travel-card">

            <h3>${h.hotel_name}</h3>

            <p>⭐ ${h.rating}</p>

            <p>₹${h.price_per_night}/night</p>

            <p>${h.address}</p>

            <a class="book-btn" target="_blank" href="${h.booking_link}">
            View Hotel
            </a>

        </div>

        `;

    });

   html += "</div>";

/* ---------------- ITINERARY ---------------- */

html += `
<h2>🗓️ Itinerary</h2>

<div class="itinerary-card">
${
    typeof marked !== "undefined"
        ? marked.parse(data.itinerary)
        : data.itinerary
}
</div>
`;

/* ---------------- AI SUMMARY ---------------- */

html += `
<h2>🤖 AI Summary</h2>
`;

html +=
typeof marked !== "undefined"
? marked.parse(data.summary)
: data.summary;

resultBox.innerHTML = html;

    resultSection.classList.remove("hidden");

}

async function sendMessage(){

    hideError();

    const message=document.getElementById("userInput").value.trim();

    if(!message){

        showError("Please enter a prompt.");

        return;

    }

    setLoading(true);

    try{

        const response=await fetch("/api/travel",{

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },

            body:JSON.stringify({

                message:message,

                thread_id:currentThreadId

            })

        });

        const data=await response.json();

        if(!response.ok||!data.success){

            throw new Error(data.error);

        }

        currentThreadId=data.thread_id;

        localStorage.setItem("travel_thread_id",currentThreadId);

        showResult(data);

    }

    catch(e){

        showError(e.message);

    }

    finally{

        setLoading(false);

    }

}

document.addEventListener("keydown",(e)=>{

    if(e.ctrlKey&&e.key==="Enter"){

        sendMessage();

    }

});