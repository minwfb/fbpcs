/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

use derive_more::TryInto;

/// The type of data stored in a column
// #[derive(Debug, PartialEq, TryInto)]
#[derive(TryInto, Clone, PartialEq, Debug)]
#[try_into(owned, ref, ref_mut)]
pub enum MPCMetricDType {
    // TODO: Will replace with MPCInt64 and such after FFI is available
    MPCInt32(i32),
    MPCInt64(i64),
    MPCUInt32(u32),
    MPCUInt64(u64),
    MPCBool(bool),
    Vec(Vec<MPCMetricDType>),
}

impl MPCMetricDType {
    pub fn take_inner_val<T>(self) -> Result<T, <T as TryFrom<MPCMetricDType>>::Error>
    where
        T: std::convert::TryFrom<MPCMetricDType>,
        <T as TryFrom<MPCMetricDType>>::Error: std::fmt::Debug,
    {
        T::try_from(self)
    }
}

#[cfg(test)]
mod tests {
    use crate::mpc_metric_dtype::MPCMetricDType;

    #[test]
    fn take_inner_val() {
        assert_eq!(
            MPCMetricDType::MPCInt32(32).take_inner_val::<i32>(),
            Ok(32i32)
        );
        assert_eq!(
            MPCMetricDType::MPCInt64(64).take_inner_val::<i64>(),
            Ok(64i64)
        );
        assert_eq!(
            MPCMetricDType::MPCUInt32(32).take_inner_val::<u32>(),
            Ok(32u32)
        );
        assert_eq!(
            MPCMetricDType::MPCUInt64(64).take_inner_val::<u64>(),
            Ok(64u64)
        );
        assert_eq!(
            MPCMetricDType::MPCBool(true).take_inner_val::<bool>(),
            Ok(true)
        );
        assert_eq!(
            MPCMetricDType::Vec(vec![MPCMetricDType::MPCBool(true)])
                .take_inner_val::<Vec::<MPCMetricDType>>(),
            Ok(vec![MPCMetricDType::MPCBool(true)])
        );

        assert!(
            MPCMetricDType::MPCUInt64(6)
                .take_inner_val::<i32>()
                .is_err()
        )
    }

    #[test]
    fn try_into() {
        assert_eq!(MPCMetricDType::MPCInt32(32).try_into(), Ok(32i32));
        assert_eq!(MPCMetricDType::MPCInt64(64).try_into(), Ok(64i64));
        assert_eq!(MPCMetricDType::MPCUInt32(32).try_into(), Ok(32u32));
        assert_eq!(MPCMetricDType::MPCUInt64(64).try_into(), Ok(64u64));
        assert_eq!(MPCMetricDType::MPCBool(true).try_into(), Ok(true));
        assert_eq!(
            MPCMetricDType::Vec(vec![MPCMetricDType::MPCBool(true)]).try_into(),
            Ok(vec![MPCMetricDType::MPCBool(true)])
        );
    }
}
