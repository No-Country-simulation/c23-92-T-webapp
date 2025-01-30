import React from "react";
import { IconProps } from "./iconTypes";

const CalendarIcon: React.FC<IconProps> = ({ className, size = 24, color = "currentColor" }) => {
  return (
    <svg width={size} height={size} viewBox="0 -4.5 157 157" fill="none" xmlns="http://www.w3.org/2000/svg" stroke={color} strokeWidth="1.57"><g id="SVGRepo_bgCarrier" strokeWidth="0"></g><g id="SVGRepo_tracerCarrier" strokeLinecap="round" strokeLinejoin="round"></g><g id="SVGRepo_iconCarrier"> <g clipPath="url(#clip0)"> <path d="M38.6174 11.6714C38.6174 9.22676 38.5662 6.98592 38.6303 4.74777C38.7093 1.9877 39.4323 0.780865 40.912 0.682198C42.3918 0.583532 43.2106 1.63988 43.6307 4.4324C43.9544 6.55568 44.1187 8.70155 44.4074 11.3357L111.435 10.7582C111.572 9.35087 111.67 8.0856 111.824 6.8276C111.983 5.54626 112.142 4.26041 112.406 2.99787C112.727 1.46659 113.641 0.46954 115.293 0.45526C117.088 0.439032 118.118 1.51198 118.405 3.16205C118.737 5.07307 118.849 7.02292 119.052 8.95601C119.108 9.4792 119.155 10.0036 119.236 10.8384C122.4 11.0026 125.478 11.2513 128.558 11.3065C142.155 11.5493 149.818 19.9339 152.541 31.7298C153.912 37.6686 154.21 43.9041 154.527 50.0292C155.266 64.2703 155.804 78.5256 156.261 92.7758C156.52 100.76 156.459 108.759 156.526 116.751C156.664 132.909 144.437 141.555 133.689 144.484C129.955 145.535 126.108 146.134 122.232 146.269C99.607 146.824 76.9766 147.444 54.3475 147.459C42.2785 147.468 30.2892 145.546 18.483 142.984C9.42075 141.019 2.43696 132.588 1.35467 122.835C1.02216 119.612 0.884885 116.371 0.943625 113.131C1.06273 102.003 1.40001 90.8771 1.44791 79.7492C1.50422 66.7862 1.37732 53.822 1.25369 40.859C1.22003 37.3038 0.990901 33.8485 2.27774 30.338C5.86768 20.5467 12.9039 15.137 22.9203 13.4298C26.9458 12.743 31.0523 12.5335 35.1213 12.0986C36.1777 11.9857 37.2205 11.8427 38.6174 11.6714ZM146.224 49.0038C123.214 49.7588 100.719 50.5615 78.2195 51.2177C55.6284 51.8792 33.0291 52.3998 10.2654 52.9867C10.2421 53.2612 10.1618 53.7787 10.1612 54.296C10.1396 71.5858 10.1259 88.8759 10.1198 106.166C10.1198 110.809 10.0959 115.457 10.3076 120.093C10.4437 123.359 11.6846 126.48 13.8258 128.945C15.9671 131.409 18.8811 133.069 22.0884 133.651C35.1639 135.873 48.2304 137.935 61.5784 137.574C73.7524 137.244 85.9379 137.36 98.115 137.112C107.807 136.917 117.497 136.538 127.179 136.098C131.402 135.878 135.481 134.485 138.96 132.073C143.656 128.901 146.812 124.747 146.914 118.766C146.994 114.125 147.293 109.484 147.221 104.844C146.948 87.2349 146.561 69.6274 146.222 52.0197C146.206 50.9564 146.226 49.8931 146.226 49.0038H146.224ZM9.40004 44.9297C54.9669 42.489 99.8116 40.8995 144.935 39.8219C144.676 37.5208 144.641 35.3429 144.158 33.2702C142.664 26.8848 139.868 21.4187 132.926 19.522C128.521 18.3185 124.004 18.6662 119.332 18.7733C119.228 19.8029 119.161 20.644 119.052 21.4795C118.962 22.3372 118.824 23.1894 118.64 24.032C117.982 26.7102 116.634 27.9266 114.556 27.7818C112.464 27.6377 111.268 26.2312 111.079 23.4744C110.971 21.9009 111.06 20.3138 111.06 18.8111H44.9162C44.9162 20.3462 44.9453 21.5109 44.9091 22.6728C44.908 24.2893 44.8215 25.9044 44.6502 27.5118C44.5905 28.2807 44.2425 28.9985 43.6763 29.5206C43.1102 30.0427 42.3679 30.3303 41.5988 30.3257C39.7863 30.4348 38.7571 29.2872 38.3558 27.7254C38.1206 26.4554 38.0189 25.1641 38.0522 23.8728C37.9939 22.4181 37.994 20.9608 37.9623 19.0998C33.0628 19.5146 28.5809 19.4471 24.3041 20.3571C17.1909 21.8715 11.3419 25.4107 10.0273 33.3618C9.42204 37.0365 9.59682 40.8415 9.40004 44.9297Z" fill={color}></path> <path d="M40.5799 123.022C39.6297 123.064 37.8043 123.217 35.9789 123.21C32.0219 123.201 29.6088 121.406 28.8728 117.563C27.9763 113.107 28.1739 108.501 29.4488 104.139C29.6864 103.195 30.1734 102.332 30.8583 101.643C31.5433 100.953 32.4009 100.461 33.3411 100.218C38.5107 98.7093 43.9077 98.1413 49.2771 98.5392C52.1537 98.7391 54.379 100.346 55.038 103.369C56.0361 107.939 56.3042 112.557 55.0633 117.131C54.0218 120.967 51.5582 122.863 47.5805 123.01C45.5428 123.084 43.4992 123.022 40.5799 123.022ZM45.3311 107.561H36.9252L37.2812 113.172H45.3311V107.561Z" fill={color}></path> <path d="M92.565 108.474C92.565 109.574 92.5799 110.223 92.565 110.871C92.3864 117.589 90.2309 120.202 83.6005 121.36C80.2125 121.952 76.7792 122.343 73.3505 122.633C69.6324 122.948 67.1364 121.288 66.4075 117.791C65.485 113.349 64.9445 108.842 65.9143 104.296C66.5965 101.101 68.4802 98.9735 71.6597 98.4984C75.9119 97.8337 80.1989 97.4156 84.4996 97.2475C89.3013 97.095 91.3889 99.0449 92.1378 103.765C92.4013 105.466 92.4511 107.202 92.565 108.474ZM82.928 106.437H73.6567C73.9674 108.86 74.2457 111.023 74.5331 113.264C76.6187 113.06 78.3237 112.908 80.0255 112.724C83.1066 112.391 83.4393 112.01 83.2931 108.865C83.2568 108.133 83.0762 107.409 82.9254 106.437H82.928Z" fill={color}></path> <path d="M115.165 121.917C113.124 122.01 111.08 121.998 109.04 121.88C105.343 121.49 103.188 119.533 102.966 115.908C102.703 111.925 102.752 107.928 103.111 103.953C103.5 99.8881 105.338 98.2296 109.408 97.909C113.371 97.5961 117.366 97.5072 121.342 97.5896C125.539 97.6772 129.492 100.381 129.181 105.915C129.029 108.608 128.982 111.317 128.636 113.987C127.974 119.09 125.479 121.329 120.323 121.718C118.605 121.848 116.885 121.938 115.166 122.046L115.165 121.917ZM111.181 105.439C111.31 108.201 111.408 110.296 111.504 112.315H119.039C119.233 110.227 119.392 108.442 119.582 106.364L111.181 105.439Z" fill={color}></path> <path d="M114.832 86.8755C113.007 86.9787 111.181 87.1813 109.357 87.1637C104.859 87.1209 102.516 84.9905 102.292 80.5304C102.118 77.0842 102.118 73.6321 102.292 70.1866C102.513 65.8732 104.062 64.0263 108.317 63.5803C113.018 63.0819 117.744 62.8762 122.47 62.9648C126.857 63.0538 129.194 65.5259 129.171 70.0133C129.123 73.6711 128.748 77.3172 128.05 80.9075C127.35 84.6458 125.106 86.3835 121.275 86.6535C119.139 86.8048 116.979 86.6808 114.829 86.6808L114.832 86.8755ZM110.3 78.1293H119.521C119.771 75.9002 119.992 73.9216 120.273 71.3998L110.3 70.959V78.1293Z" fill={color}></path> <path d="M63.3293 75.4114C63.5449 73.2693 63.6808 71.0026 64.0226 68.7644C64.411 66.2328 65.6701 64.2777 68.3597 63.7298C73.1173 62.7607 77.9009 61.938 82.7868 62.5203C87.0531 63.0279 89.3679 64.8488 89.9595 69.1156C90.3544 72.3093 90.3019 75.5432 89.8048 78.7226C89.3064 82.1629 86.8758 84.2297 83.4256 84.6822C79.2622 85.2274 75.0754 85.6611 70.8861 85.9194C66.8366 86.17 64.3851 84.098 63.6854 80.0585C63.4303 78.5791 63.4472 77.0511 63.3293 75.4114ZM80.8138 71.1434L71.156 70.5028C71.3068 72.9116 71.4227 74.7688 71.556 76.8947L80.8125 75.9619L80.8138 71.1434Z" fill={color}></path> </g> <defs> <clipPath id="clip0"> <rect width="156" height="190" fill="white" transform="translate(0.777344)"></rect> </clipPath> </defs> </g></svg>
   
  );
};

export default CalendarIcon;