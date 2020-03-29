import {Component, OnInit} from '@angular/core';
import {interval, Subscription} from 'rxjs';

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
  timer = interval(1000);
  subscription: Subscription;

  constructor() {
  }

  ngOnInit(): void {
    this.subscription = this.timer.subscribe(_ => {
      const date = new Date();
      this.hour = date.getHours().toString();
      this.minute = date.getMinutes().toString();
      this.separator = this.separator === ":" ? "&nbsp;" : ":";
      const options = {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};
      this.date = date.toLocaleDateString("en-US", options)
    })
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe()
  }
}
