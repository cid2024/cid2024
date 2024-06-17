// globalStyled.js
import styled from "styled-components";
import theme from "./theme.js";
const parser = (value) => {
  if (typeof value === "string") {
    if (value.substring(value.length - 2, value.length) == "px") {
      return value;
    } else if (value.substring(value.length - 1, value.length) === "%") {
      return value;
    } else {
      return value + "px";
    }
  } else {
    return value + "px";
  }
};
export const Col = styled.div`
  display: flex;
  flex-direction: column;
  width: ${(props) => (props.width ? parser(props.width) : "100%")};
  height: ${(props) => (props.height ? parser(props.height) : "100%")};
  justify-content: ${(props) =>
    props.justifyContent ? props.justifyContent : "center"};
  align-items: ${(props) => (props.alignItems ? props.alignItems : "center")};
`;
// export const GlobalStyled = {
export const Row = styled.div`
  display: flex;
  flex-direction: row;
  width: ${(props) => (props.width ? parser(props.width) : "100%")};
  height: ${(props) => (props.height ? parser(props.height) : "100%")};
  justify-content: ${(props) =>
    props.justifyContent ? props.justifyContent : "center"};
  align-items: ${(props) => (props.alignItems ? props.alignItems : "center")};
`;
export const Noto1 = styled.div`
  font-size: 24px;
  font-weight: ${(props) =>
    props.fontWeight ? fontWeight[props.fontWeight] : "700"};
  font-family: ${(props) =>
    props.fontWeight ? fontFamily[props.fontWeight] : "NotoSansKR-Bold"};
  include-font-padding: false;
  color: ${(props) => (props.color ? props.color : theme.BlackGray)};
`;
export const Noto2 = styled.div`
  font-size: 19px;
  font-weight: ${(props) =>
    props.fontWeight ? fontWeight[props.fontWeight] : "700"};
  font-family: ${(props) =>
    props.fontWeight ? fontFamily[props.fontWeight] : "NotoSansKR-Bold"};
  include-font-padding: false;
  color: ${(props) => (props.color ? props.color : theme.BlackGray)};
`;
export const Noto3 = styled.div`
  font-size: 16px;
  font-weight: ${(props) =>
    props.fontWeight ? fontWeight[props.fontWeight] : "700"};
  font-family: ${(props) =>
    props.fontWeight ? fontFamily[props.fontWeight] : "NotoSansKR-Bold"};
  include-font-padding: false;
  color: ${(props) => (props.color ? props.color : theme.BlackGray)};
`;
export const Noto4 = styled.div`
  font-size: 14px;
  font-weight: ${(props) =>
    props.fontWeight ? fontWeight[props.fontWeight] : "700"};
  font-family: ${(props) =>
    props.fontWeight ? fontFamily[props.fontWeight] : "NotoSansKR-Bold"};
  color: ${(props) => (props.color ? props.color : theme.BlackGray)};
  include-font-padding: false;
`;
export const Noto5 = styled.div`
  font-size: 12px;
  font-weight: ${(props) =>
    props.fontWeight ? fontWeight[props.fontWeight] : "700"};
  font-family: ${(props) =>
    props.fontWeight ? fontFamily[props.fontWeight] : "NotoSansKR-Bold"};
  color: ${(props) => (props.color ? props.color : theme.BlackGray)};
  include-font-padding: false;
`;
export const Noto6 = styled.div`
  font-size: 10px;
  font-weight: ${(props) =>
    props.fontWeight ? fontWeight[props.fontWeight] : "700"};
  font-family: ${(props) =>
    props.fontWeight ? fontFamily[props.fontWeight] : "NotoSansKR-Bold"};
  color: ${(props) => (props.color ? props.color : theme.BlackGray)};
  include-font-padding: false;
`;
export const WhiteSpace = styled.div`
  height: ${(props) => (props.height ? parser(props.height) : "10px")};
  width: ${(props) => (props.width ? parser(props.width) : "10px")};
`;
const fontWeight = {
  Light: "100",
  Regular: "400",
  Medium: "500",
  Bold: "700",
};
const fontFamily = {
  Light: "NotoSansKR-Thin",
  Regular: "NotoSansKR-Regular",
  Medium: "NotoSansKR-Medium",
  Bold: "NotoSansKR-Bold",
};