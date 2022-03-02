import type { Entry } from "../stork";
import { writable } from "svelte/store";

// stores selected table and shouldShowSideBar
const tableStore = writable<[Entry, boolean]>([null, false]);
export default tableStore;
