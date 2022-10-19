window.onload = function(){
    let type_bar = document.getElementById("type_filter");
    let type_all = document.getElementById("all");
    let type_loaned = document.getElementById("loaned");
    let type_unloaned = document.getElementById("unloaned");
    let table = document.getElementsByTagName("tbody")[0];
    let items = [];
    type_all.onclick = function(){
        loadAll(table, items);   
    }
    type_loaned.onclick = function(){
        loadLoaned(table, items); 
    }
    type_unloaned.onclick = function(){
        loadUnloaned(table, items); 
    }
    let user_els = document.getElementsByTagName('mything');
    for (let i = 0; i< user_els.length; i++)
    {
        let new_item = {
            'name': user_els[i].attributes.name.value,
            'status': user_els[i].attributes.status.value,
            'value': user_els[i].attributes.value.value,
            'rate': user_els[i].attributes.rate.value
        }
        items.push(new_item);
    }
    loadAll(table, items);
}

function loadAll(table, items)
{
    clearTable();
    items.forEach(item => {
        console.log(item);
        loadOne(table, item);
    })
}

function loadLoaned(table, items)
{
    clearTable();
    items.forEach
    (
        item => 
        {
            if (item.status == 'loaned')
            {
                loadOne(table, item);
            }
        }
    )
}

function loadUnloaned(table, items)
{
    clearTable();
    items.forEach
    (
        item => 
        {
            if (item.status == 'unloaned')
            {
                loadOne(table, item);
            }
        }
    )
}

function clearTable()
{
    let table = document.getElementsByTagName("tbody")[0];
    let row_count = table.childElementCount;
    for (let i = 1; i<row_count; i++)
    {
        table.removeChild(table.lastChild);
    }
}

function loadOne(table, item)
{
    let new_el = document.createElement('tr');
    new_el.className = "normal_row";  
    let el_name = document.createElement('td');
    el_name.innerHTML = item.name;
    new_el.appendChild(el_name);
    let el_value = document.createElement('td');
    el_value.innerHTML = item.value;
    new_el.appendChild(el_value);
    let el_rate = document.createElement('td');
    el_rate.innerHTML = item.rate;
    new_el.appendChild(el_rate);
    let el_status = document.createElement('td');
    el_status.innerHTML = item.status;
    new_el.appendChild(el_status);
    table.appendChild(new_el);
}