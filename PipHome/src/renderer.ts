/**
 * This file will automatically be loaded by webpack and run in the "renderer" context.
 * To learn more about the differences between the "main" and the "renderer" context in
 * Electron, visit:
 *
 * https://electronjs.org/docs/tutorial/application-architecture#main-and-renderer-processes
 *
 * By default, Node.js integration in this file is disabled. When enabling Node.js integration
 * in a renderer process, please be aware of potential security implications. You can read
 * more about security risks here:
 *
 * https://electronjs.org/docs/tutorial/security
 *
 * To enable Node.js integration in this file, open up `main.js` and enable the `nodeIntegration`
 * flag:
 *
 * ```
 *  // Create the browser window.
 *  mainWindow = new BrowserWindow({
 *    width: 800,
 *    height: 600,
 *    webPreferences: {
 *      nodeIntegration: true
 *    }
 *  });
 * ```
 */

import './index.css';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import '../node_modules/bootstrap/dist/js/bootstrap.bundle.min.js'

import {timer} from 'rxjs';

const $: JQueryStatic = require("jquery");
const {readFileSync} = require('fs');

document.querySelector('#hour').innerHTML = '22';

const navClock = $("#nav-clock");
const navHome = $("#nav-home");
const navMisc = $("#nav-misc");

function deactivateWholeNavbar() {
	navClock.removeClass('active');
	navHome.removeClass('active');
	navMisc.removeClass('active');
}

navClock.on("click", function () {
	deactivateWholeNavbar();
	navClock.addClass('active');
	$("#main-content").html(readFileSync("./src/clock.html", {encoding: "UTF-8"}));
});

navHome.on("click", function () {
	deactivateWholeNavbar();
	navHome.addClass('active');
	$("#main-content").html(readFileSync("./src/home.html", {encoding: "UTF-8"}));
});

navMisc.on("click", function () {
	deactivateWholeNavbar();
	navMisc.addClass('active');
	$("#main-content").html(readFileSync("./src/misc.html", {encoding: "UTF-8"}));
});

// CLOCK NAV
function buildTwoDigitsString(number: number): string {
	if (number > 9) {
		return number.toString();
	} else {
		return "0" + number.toString();
	}
}

const subscription = timer(0, 1000).subscribe(next => {
	const date = new Date();
	$('#hour').text(buildTwoDigitsString(date.getHours()));
	$('#minute').text(buildTwoDigitsString(date.getMinutes()));
	$('#separator').html(next % 2 === 0 ? "&nbsp;" : ":");
	const options = {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};
	$('#date').text(date.toLocaleDateString("en-US", options));
});