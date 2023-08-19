function ordinal_suffix_of(i) {
    var j = i % 10,
        k = i % 100;
    if (j == 1 && k != 11) {
        return i + "st";
    }
    if (j == 2 && k != 12) {
        return i + "nd";
    }
    if (j == 3 && k != 13) {
        return i + "rd";
    }
    return i + "th";
}

function pad(x) {
    if (x < 10) return "0" + x;
    return x;
}

const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
const months = ["Jan", "Feb", "Mar", "April", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

function getFormattedDateString(date) {
    var day_and_month = ordinal_suffix_of(date.getDate()) + " " + months[date.getMonth()] + " " + date.getFullYear()
    return days[date.getDay()] + ' (' + day_and_month + ') ' + pad(date.getHours()) + ':' + pad(date.getMinutes());
}
