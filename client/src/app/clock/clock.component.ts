import {Component, OnInit} from '@angular/core';
import {Subscription, timer} from 'rxjs';

@Component({
  selector: 'app-clock',
  templateUrl: './clock.component.html',
  styleUrls: ['./clock.component.sass']
})
export class ClockComponent implements OnInit {
  hour: string = "&nbsp;&nbsp;";
  minute: string = "&nbsp;&nbsp;";
  separator: string = "&nbsp;";
  date: string = "";
  timer = timer(0, 1000);
  subscription: Subscription;

  constructor() {
  }

  ngOnInit(): void {
    this.subscription = this.timer.subscribe(_ => {
      const date = new Date();
      this.hour = this.buildTwoDigitsString(date.getHours());
      this.minute = this.buildTwoDigitsString(date.getMinutes());
      this.separator = this.separator === ":" ? "&nbsp;" : ":";
      const options = {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};
      this.date = date.toLocaleDateString("en-US", options)
    })
  }

  buildTwoDigitsString(number: number) {
    if (number > 9) {
      return number.toString();
    } else {
      return "0" + number.toString();
    }
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe()
  }
}
