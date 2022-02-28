export type ColList = Array<{ checked: boolean; col: string; colName: string }>;
export type DataSet = { [table: string]: { tableName: string; cols: { [col: string]: string } } };
