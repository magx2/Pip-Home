import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {ClockComponent} from './clock/clock.component';
import {MiscComponent} from './misc/misc.component';

@NgModule({
  declarations: [
    AppComponent,
    ClockComponent,
    MiscComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
