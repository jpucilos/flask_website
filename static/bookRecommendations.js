 var spData = null;

  function doData(json) {
      spData = json.feed.entry;
  }

  function drawCell(tr, val, isHeader) {
      var td = $(isHeader ? "<th/>" : "<td/>");
      tr.append(td);
      td.append(val);
      return td;
  }

  function drawRow(table, rowData, isHeader) {
      if (rowData == null) return null;
      if (rowData.length == 0) return null;
      var tr = $("<tr/>");
      if (isHeader) tr.addClass("head");
      table.append(tr);
      for (var c = 0; c < rowData.length; c++) {
          drawCell(tr, rowData[c], ((c == 0) || isHeader));
      }
      return tr;
  }

  function drawTable(parent) {
      var table = $("<table/>");
      parent.append(table);
      return table;
  }

  function readData(parent) {
      var data = spData;
      var table = drawTable(parent);
      var rowData = [];
      var row = 0;

      for (var r = 0; r < data.length; r++) {
          var cell = data[r]["gs$cell"];
          var val = cell["$t"];
          if (cell.col == 1) {
              drawRow(table, rowData, (row == 1));
              rowData = [];
              row++;
          }
          rowData.push(val);
      }
      drawRow(table, rowData, (row == 1));
  }
  $(document).ready(function () {
      readData($("#data"));
  });