$(document).ready(function() {
    Object.size = function(obj) {
        var size = 0,
            key;
        for (key in obj) {
            if (obj.hasOwnProperty(key)) size++;
        }
        return size;
    };

    function deleteRow(tableID, rowNum) {
        document.getElementById(tableID).deleteRow(rowNum);
    };

    // change timestamp
    function timetrans(date) {
        var date = new Date(date * 1000); //如果date为13位不需要乘1000
        var Y = date.getFullYear() + '-';
        var M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-';
        var D = (date.getDate() < 10 ? '0' + (date.getDate()) : date.getDate()) + ' ';
        var h = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours()) + ':';
        var m = (date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()) + ':';
        var s = (date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds());
        return Y + M + D + h + m + s;
    }

    function addRow(tableID, it, rid, name, rtime) {
        // Get a reference to the table
        let tableRef = document.getElementById(tableID);

        // Insert a row at the end of the table
        let newRow = tableRef.insertRow(-1);

        let newCell1 = newRow.insertCell(0);
        let newText1 = document.createTextNode(it + 1);
        newCell1.appendChild(newText1);

        let newCell2 = newRow.insertCell(1);
        let newText2 = document.createTextNode(name);
        newCell2.appendChild(newText2);

        let newCell3 = newRow.insertCell(2);
        let newText3 = document.createTextNode(rid);
        newCell3.appendChild(newText3);

        let newCell4 = newRow.insertCell(3);
        let newText4 = document.createTextNode(rtime);
        newCell4.appendChild(newText4);

        if (tableID == "theTable") {
            let newCell5 = newRow.insertCell(4);
            newCell5.innerHTML = "<input class='btn btn-success' type='submit' value='Check In' id = 'accept'>";
        } else {
            let newCell5 = newRow.insertCell(4);
            newCell5.innerHTML = "<input class='btn btn-success' type='submit' value='Check Out' id = 'checkOut'></input>";
        }
    }

    $.post("/get-students", {
            state: 2,
        },
        function(response) {
            console.log(response.code);
            var size = Object.size(response.data);
            console.log(size);
            var i;
            for (i = 0; i < size; i++) {
                var stuid = response.data[i].id;
                var name = response.data[i].name;
                var ts = response.data[i].ts;
                addRow("theTable", i, stuid, name, timetrans(ts));
            }
            //console.log(data.data);
        });

    $.post("/get-students", {
            state: 3,
        },
        function(response) {
            console.log(response.code);
            var size = Object.size(response.data);
            console.log(size);
            var i;
            for (i = 0; i < size; i++) {
                var stuid = response.data[i].id;
                var name = response.data[i].name;
                var ts = response.data[i].ts;

                addRow("theTable2", i, stuid, name, timetrans(ts));
            }
            //console.log(data.data);
        });

    //Check In function
    $("#theTable").on('click', '#accept', function() {
        var row = $(this).closest('tr'),
            cells = row.find('td'),
            btnCell = $(this).parent();
        var rowInd = row.index();
        console.log(rowInd);
        console.log(cells[2].innerHTML + " Accpet");
        var stuid = cells[2].innerHTML;
        $.post("/update-state", {
                id: stuid,
                state: 3,
            },
            function(data) {
                if (data.code) {
                    alert("An Unexpected Error has occured. Please Refresh the Page and Try Again");
                } else {
                    alert("You Checked in " + stuid + " to Library");
                }
            });
        deleteRow("theTable", rowInd);

    });

    //check out function
    $("#theTable2").on('click', '#checkOut', function() {
        var row = $(this).closest('tr'),
            cells = row.find('td'),
            btnCell = $(this).parent();
        console.log(cells[2].innerHTML + " Checked Out");
        var stuid = cells[2].innerHTML;
        var rowInd = row.index();
        console.log(rowInd);

        $.post("/update-state", {
                id: stuid,
                state: 4,
            },
            function(data) {
                if (data.code) {
                    alert("An Unexpected Error has occured. Please Refresh the Page and Try Again");
                } else {
                    alert("You Checked out " + stuid);
                }
            });
        deleteRow("theTable2", rowInd);
    });

});
