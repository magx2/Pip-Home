import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {ClockComponent} from "./clock/clock.component";
import {MiscComponent} from "./misc/misc.component";
import {HomeComponent} from "./home/home.component";


const routes: Routes = [
  {path: "misc", component: MiscComponent},
  {path: "home", component: HomeComponent},
  {path: "", component: ClockComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
