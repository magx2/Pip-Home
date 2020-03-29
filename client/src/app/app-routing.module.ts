import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {ClockComponent} from "./clock/clock.component";
import {MiscComponent} from "./misc/misc.component";


const routes: Routes = [
  {path: "misc", component: MiscComponent},
  {path: "", component: ClockComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
