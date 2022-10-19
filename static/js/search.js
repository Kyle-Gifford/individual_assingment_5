window.onload = function(){
    hideTable();
    let full_table = document.getElementsByTagName('table')[0];
    let table = document.getElementsByTagName("tbody")[0];
    let items = [];
    let search_bar = document.getElementById('query_string');
    let user_els = document.getElementsByTagName('mything');
    for (let i = 0; i< user_els.length; i++)
    {
        let new_item = {
            'name': user_els[i].attributes.name.value,
            'status': user_els[i].attributes.status.value,
            'value': user_els[i].attributes.value.value,
            'rate': user_els[i].attributes.rate.value,
            'id': user_els[i].attributes.id.value
        }
        items.push(new_item);
    }
    search_bar.onkeyup = function()
    {
        key_changed(items, search_bar, table);
    }
}

function key_changed(items, search_bar, table)
{
    hideTable();
    clearTable();
    let query_string = search_bar.value;
    if (query_string.length > 0)
    {
        items.forEach(item => {
            if (item.name.toLowerCase().includes(query_string.toLowerCase()))
            {
                loadOne(table, item);
            }
        })
        if (table.childElementCount > 1)
        {
            showTable();
        }
    }
}


function showTable()
{
    document.getElementsByTagName('table')[0].style.display = 'block';
}

function hideTable()
{
    document.getElementsByTagName('table')[0].style.display = 'none';
}

function loadAll(table, items)
{
    clearTable();
    items.forEach(item => {
        console.log(item);
        loadOne(table, item);
    })
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
    let el_view = document.createElement('td');
    el_view.innerHTML = '<a href="/view/' + item.id + '">View</a>';
    new_el.appendChild(el_view);
    let el_borrow = document.createElement('td');
    el_borrow.innerHTML = '<a href="/borrow/' + item.id + '">Borrow</a>';
    new_el.appendChild(el_borrow);
    new_el.id = item.id
    table.appendChild(new_el);
}