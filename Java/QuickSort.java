package com.shyling;

import java.util.Arrays;

public class QuickSort {


    public static void qsort(int[] arr,int start,int end){
        if(start<end){
            int pivot = arr[start];
            int l = start,r=end;
            while(l<r){
                while(l<r && arr[r]>pivot){
                    r--;
                }
                arr[l] = arr[r];
                while (l<r && arr[l]<pivot){
                    l++;
                }
                arr[l] = arr[r];
            }
            arr[l] = pivot;
            qsort(arr,start,l-1);
            qsort(arr,l+1,end);
        }
    }

    public static void main(String[] args) {
        int[] arr = new int[]{10,9,8,7,6,5,4,3,2,1};
        qsort(arr,0,arr.length-1);
        System.out.println(Arrays.toString(arr));
    }
}
