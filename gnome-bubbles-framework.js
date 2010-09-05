/*
    This file is part of gnome-bubbles.

    gnome-bubbles is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    gnome-bubbles is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with gnome-bubbles.  If not, see <http://www.gnu.org/licenses/>.
*/

SSB = function() {
    var bla;
    function privateFunction() {
        return true;
    }
    return {
        sendCommandToPython: function(object, command) {
            oldtitle = document.title;
            document.title="GNOME-BUBBLES:"+object+"::"+command;
            document.title=oldtitle;
        },
        escapeData: function(data) {
            data = data.toString();
            return data.replace(/,/g,'\\,');
        },
        notify: function(html,width,height,delay) {
            alert('notification');
        }
    };
} ();


SSB.contextMenu = function() {
    var objectName = 'SSB.contextMenu';
    function privateFunction() {
        return true;
    }
    return {
        add: function(title, action, disable) {
            title = SSB.escapeData(title);
            action = SSB.escapeData(action);
            if (!disable) {disable = false;}
            SSB.sendCommandToPython(objectName,"add,"+title+","+action+","+disable);
        }
    };
} ();

