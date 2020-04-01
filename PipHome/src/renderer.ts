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

document.querySelector('#hour').innerHTML = '22';

function buildTwoDigitsString(number: number): string {
	if (number > 9) {
		return number.toString();
	} else {
		return "0" + number.toString();
	}
}

const subscription = timer(0, 1000).subscribe(next => {
	const date = new Date();
	document.querySelector('#hour').innerHTML = buildTwoDigitsString(date.getHours());
	document.querySelector('#minute').innerHTML = buildTwoDigitsString(date.getMinutes());
	document.querySelector('#separator').innerHTML = next % 2 === 0 ? "&nbsp;" : ":";
	const options = {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};
	document.querySelector('#date').innerHTML = date.toLocaleDateString("en-US", options)
});