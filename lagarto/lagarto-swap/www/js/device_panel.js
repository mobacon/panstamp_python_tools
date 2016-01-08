/* Copyright (c) Daniel Berenguer (panStamp) 2012 */

/**
 * Update table fields
 */
function updateValues()
{
  var jsonDoc = getJsonDoc();
  var swapnet = jsonDoc.network;

  if (swapnet.motes.length == 0)
    document.getElementById("nodev").style.display='block';
  else
    swapnet.motes.forEach(addMote);
}

/**
 * Add mote
 */
function addMote(mote)
{
  var nettable = document.getElementById("nettable");
  var row, cell, label, cfglink, img;

  row = nettable.insertRow(nettable.rows.length);

  // Address
  cell = row.insertCell(0);
  label = document.createTextNode(mote.address);
  cell.appendChild(label);
  // Developer
  cell = row.insertCell(1);
  label = document.createTextNode(mote.manufacturer);
  cell.appendChild(label);
  // Description
  cell = row.insertCell(2);
  label = document.createTextNode(mote.name);
  cell.appendChild(label);
  // Action
  // Edit device
  cell = row.insertCell(3);
  cfglink = document.createElement("a");
  cfglink.setAttribute("href", "/config_device.html?address=" + mote.address);
  cell.appendChild(cfglink);
  img = document.createElement("img");
  img.setAttribute("src","/lagarto/images/edit.png");
  img.title = "edit";
  cfglink.appendChild(img);
  // Insert blank space
  cell.appendChild( document.createTextNode('\u00A0\u00A0'));
  // Delete device
  cfglink = document.createElement("a");
  cfglink.setAttribute("href", "/command/delete_mote?address=" + mote.address);
  cfglink.onclick = function() {return confirm("Delete mote?");};
  cfglink.setAttribute("alt", "delete");
  cfglink.style.pointer = "cursor";
  cell.appendChild(cfglink);
  img = document.createElement("img");
  img.setAttribute("src","/lagarto/images/delete.png");
  img.title = "delete";
  cfglink.appendChild(img);
}

